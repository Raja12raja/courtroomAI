"""Sidebar: language selector and about text."""

from __future__ import annotations

import streamlit as st

from courtroom_core import LANGUAGE_NAMES

from courtroom_ui.i18n import tr
from courtroom_ui.session import reset_simulation


def render_sidebar() -> None:
    """Language widget, about copy, and simulation reset when language changes."""
    # Initialize language state if needed
    if "selected_language" not in st.session_state:
        st.session_state.selected_language = "en"

    if "language_selector" not in st.session_state:
        st.session_state.language_selector = st.session_state.selected_language

    # Update selected language BEFORE any tr() calls
    if st.session_state.language_selector != st.session_state.selected_language:
        st.session_state.selected_language = st.session_state.language_selector
        reset_simulation()

    with st.sidebar:
        st.markdown(tr("lang_title"))

        st.selectbox(
            tr("select_interface_language"),
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES[x],
            key="language_selector",
        )

        st.markdown("---")
        st.markdown(
            f"""
{tr("about_app")}

{tr("about_desc")}
* Test legal arguments
* Analyze evidence credibility
* Get strategic recommendations
* Understand case strengths & weaknesses

{tr("about_langs")}
* English
* Hindi (हिंदी)
* Tamil (தமிழ்)
* Telugu (తెలుగు)
* Bengali (বাংলা)
* Marathi (मराठी)
* Gujarati (ગુજરાતી)
* Kannada (ಕನ್ನಡ)
* Malayalam (മലയാളം)
"""
        )
