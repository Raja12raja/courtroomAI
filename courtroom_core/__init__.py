"""
Courtroom simulation engine: RAG, agents, evidence, and scoring.

Prefer ``from courtroom_core import ...`` in new code; ``backend`` re-exports the same API.
"""
from __future__ import annotations

from .agents import (
    judge_ai,
    lawyer_ai,
    lawyer_ai_with_evidence,
    lawyer_ai_with_options,
    opponent_ai,
)
from .credibility import check_evidence_credibility
from .documents import (
    describe_image_with_vision,
    extract_pdf_text,
    extract_text_from_image,
    image_to_base64,
    process_evidence_file,
    process_image_file,
)
from .json_utils import extract_json_from_text
from .llm import ask_llm, get_client
from .locales import (
    LANGUAGE_NAMES,
    TRANSLATIONS,
    get_language_instruction,
    get_translation,
)
from .rag import search
from .scoring import compute_win_probability
from .simulation import (
    run_interactive_round,
    run_simulation,
    start_interactive_simulation,
)

__all__ = [
    "LANGUAGE_NAMES",
    "TRANSLATIONS",
    "ask_llm",
    "check_evidence_credibility",
    "compute_win_probability",
    "describe_image_with_vision",
    "extract_json_from_text",
    "extract_pdf_text",
    "extract_text_from_image",
    "get_client",
    "get_language_instruction",
    "get_translation",
    "image_to_base64",
    "judge_ai",
    "lawyer_ai",
    "lawyer_ai_with_evidence",
    "lawyer_ai_with_options",
    "opponent_ai",
    "process_evidence_file",
    "process_image_file",
    "run_interactive_round",
    "run_simulation",
    "search",
    "start_interactive_simulation",
]
