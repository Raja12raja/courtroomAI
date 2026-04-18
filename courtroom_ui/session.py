"""Streamlit session defaults and simulation lifecycle."""

from __future__ import annotations

import streamlit as st

_SESSION_DEFAULTS: dict[str, object] = {
    "error": None,
    "interactive_state": None,
    "round_phase": None,
    "completed_rounds": [],
}


def ensure_session_state() -> None:
    """Populate `st.session_state` keys used by the courtroom UI."""
    for key, value in _SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_simulation() -> None:
    """Clear hearing progress and errors."""
    st.session_state.error = None
    st.session_state.interactive_state = None
    st.session_state.round_phase = None
    st.session_state.completed_rounds = []
