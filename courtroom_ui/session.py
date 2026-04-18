"""Streamlit session defaults and simulation lifecycle."""

from __future__ import annotations

import streamlit as st

_SESSION_DEFAULTS: dict[str, object] = {
    "error": None,
    "interactive_state": None,
    "round_phase": None,
    "completed_rounds": [],
    "selected_language": "en",
    "language_selector": "en",
}


def ensure_session_state() -> None:
    """Populate `st.session_state` keys used by the courtroom UI."""
    for key, value in _SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Ensure selected_language always matches language_selector on initialization
    if "language_selector" in st.session_state and "selected_language" in st.session_state:
        if st.session_state.selected_language != st.session_state.language_selector:
            st.session_state.selected_language = st.session_state.language_selector


def reset_simulation() -> None:
    """Clear hearing progress and errors, but preserve language selection."""
    st.session_state.error = None
    st.session_state.interactive_state = None
    st.session_state.round_phase = None
    st.session_state.completed_rounds = []
    # DON'T reset language settings here - they should persist