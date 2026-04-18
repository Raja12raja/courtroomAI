"""Inject global Streamlit custom CSS from a static stylesheet."""

from pathlib import Path

import streamlit as st

from courtroom_ui.config import PACKAGE_DIR

_CSS_PATH = PACKAGE_DIR / "static" / "app.css"


def inject_app_styles() -> None:
    """Load `static/app.css` and push it into the page via `st.markdown`."""
    css = _CSS_PATH.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
