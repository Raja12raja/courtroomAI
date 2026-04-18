"""Sidebar: language selector and about text."""

from __future__ import annotations

import streamlit as st

from courtroom_core import LANGUAGE_NAMES

from courtroom_ui.i18n import tr
from courtroom_ui.session import reset_simulation


def render_sidebar() -> None:
    """Language widget, about copy, and simulation reset when language changes."""
    
    with st.sidebar:
        st.markdown(tr("lang_title"))

        # Store the previous language before rendering selectbox
        prev_language = st.session_state.get("selected_language", "en")
        
        st.selectbox(
            tr("select_interface_language"),
            options=list(LANGUAGE_NAMES.keys()),
            format_func=lambda x: LANGUAGE_NAMES[x],
            key="language_selector",
        )
        
        # Only reset if language actually changed (not just on rerun)
        current_language = st.session_state.language_selector
        if current_language != prev_language:
            st.session_state.selected_language = current_language
            # Only reset if there's an active simulation to reset
            if st.session_state.get("interactive_state") is not None:
                reset_simulation()

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