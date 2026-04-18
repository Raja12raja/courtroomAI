"""UI translation tables, disk cache, and the `tr()` lookup helper."""

from __future__ import annotations

import json
from typing import Any

import streamlit as st

from courtroom_core import ask_llm

from courtroom_ui.config import UI_CACHE_FILE
from courtroom_ui.strings import UI_TRANSLATIONS


def _extract_json_dict(raw_text: str) -> dict[str, Any]:
    text = raw_text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        if text.startswith("json"):
            text = text[4:].strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return {}
    try:
        obj = json.loads(text[start : end + 1])
        return obj if isinstance(obj, dict) else {}
    except Exception:
        return {}


def _load_persistent_ui_cache() -> dict[str, Any]:
    if not UI_CACHE_FILE.exists():
        return {}
    try:
        with UI_CACHE_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _save_persistent_ui_cache(cache: dict[str, Any]) -> None:
    try:
        with UI_CACHE_FILE.open("w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False)
    except Exception:
        pass


def get_ui_translations(language: str) -> dict[str, str]:
    """Return UI strings for `language`, using session cache, disk cache, or LLM fallback."""
    if language in UI_TRANSLATIONS:
        return UI_TRANSLATIONS[language]

    if language == "en":
        return UI_TRANSLATIONS["en"]

    cache_key = f"ui_translations_{language}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    persistent_cache = _load_persistent_ui_cache()
    if language in persistent_cache and isinstance(persistent_cache[language], dict):
        merged_cached = {
            **UI_TRANSLATIONS["en"],
            **{k: v for k, v in persistent_cache[language].items() if isinstance(v, str)},
        }
        st.session_state[cache_key] = merged_cached
        return merged_cached

    base = UI_TRANSLATIONS["en"]
    prompt = (
        "Translate the JSON values below into the target language for a legal app UI. "
        "Keep keys exactly the same. Preserve emojis and punctuation. "
        "Return ONLY valid JSON object with same keys.\n\n"
        f"Target language code: {language}\n"
        f"JSON:\n{json.dumps(base, ensure_ascii=False)}"
    )

    try:
        translated_raw = ask_llm(
            prompt,
            system="You are a professional UI translator. Return strict JSON only.",
            language=language,
        )
        translated = _extract_json_dict(translated_raw)
        merged = {**base, **{k: v for k, v in translated.items() if isinstance(v, str)}}
        st.session_state[cache_key] = merged

        persistent_cache[language] = {k: v for k, v in merged.items() if isinstance(v, str)}
        _save_persistent_ui_cache(persistent_cache)

        return merged
    except Exception:
        return base


def tr(key: str) -> str:
    """Translate `key` for the sidebar-selected interface language."""
    language = st.session_state.get("selected_language", "en")
    translations = get_ui_translations(language)
    return translations.get(key, UI_TRANSLATIONS["en"].get(key, key))
