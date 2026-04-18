"""
Courtroom AI — Streamlit entrypoint.

UI layout lives under `courtroom_ui/` (styles, i18n, sidebar, hearing flow).
"""

from __future__ import annotations
import time
import streamlit as st
from courtroom_core import run_interactive_round, start_interactive_simulation

from courtroom_ui.components import hearing_loader_markup
from courtroom_ui.config import PAGE_ICON, PAGE_TITLE
from courtroom_ui.hearing_flow import render_hearing_flow
from courtroom_ui.i18n import tr
from courtroom_ui.session import ensure_session_state, reset_simulation
from courtroom_ui.sidebar import render_sidebar
from courtroom_ui.styles import inject_app_styles


def main() -> None:
    st.set_page_config(
        page_title=PAGE_TITLE,
        page_icon=PAGE_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    ensure_session_state()

    render_sidebar()
    inject_app_styles()

    st.markdown(f'<div class="main-title">{tr("header_title")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="subtitle">{tr("header_subtitle")}</div>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    user_case = st.text_area(
        tr("describe_case"),
        placeholder=tr("case_placeholder"),
        height=160,
        label_visibility="visible",
    )
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button(tr("start_hearing"))
    
    if run_btn:
        if not user_case.strip():
            st.warning(tr("warning_enter_case"))
        else:
            reset_simulation()
            language = st.session_state.selected_language
            loader_slot = st.empty()
            loader_slot.markdown(
                hearing_loader_markup(tr("loader_hearing_title"), tr("spinner_init")),
                unsafe_allow_html=True,
            )
            time.sleep(0.06)
            try:
                state = start_interactive_simulation(user_case.strip(), language)
                st.session_state.interactive_state = state
                round_result = run_interactive_round(state)
                st.session_state.round_phase = round_result
            except Exception as e:
                st.session_state.error = str(e)
            finally:
                loader_slot.empty()

    if st.session_state.error:
        st.error(f"{tr('sim_failed')}: {st.session_state.error}")

    if st.session_state.interactive_state and st.session_state.round_phase:
        render_hearing_flow()


main()
