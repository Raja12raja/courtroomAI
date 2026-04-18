"""Interactive hearing: rounds, evidence, credibility, and final verdict."""
import time

import streamlit as st

from courtroom_core import compute_win_probability, run_interactive_round

from courtroom_ui.components import hearing_loader_markup
from courtroom_ui.i18n import tr
from courtroom_ui.session import reset_simulation


def render_hearing_flow() -> None:
    state = st.session_state.interactive_state
    phase = st.session_state.round_phase
    language = state.get("language", "en")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # Show context
    if st.session_state.completed_rounds == []:
        with st.expander(tr("legal_context"), expanded=False):
            st.markdown(f"<div style='color:#8a8577; font-size:0.87rem; line-height:1.7'>{state['context'][:400]}...</div>", unsafe_allow_html=True)

    # Display completed rounds
    for round_data in st.session_state.completed_rounds:
        rn = round_data["round"]
        judge = round_data["judge"]

        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {rn} - {tr("round_completed")}</div>', unsafe_allow_html=True)

        col_opp, col_law = st.columns(2)

        with col_opp:
            st.markdown(f"""
            <div class="agent-card opponent-card">
                <div class="agent-label" style="color:#c0392b">{tr("opposing_counsel")}</div>
                {round_data['opponent']}
            </div>
            """, unsafe_allow_html=True)

        with col_law:
            st.markdown(f"""
            <div class="agent-card lawyer-card">
                <div class="agent-label" style="color:#27ae60">{tr("defense_lawyer")}</div>
                {round_data['lawyer']}
            </div>
            """, unsafe_allow_html=True)

        # Judge evaluation
        d_score = judge.get("defense_score", "?")
        p_score = judge.get("prosecution_score", "?")
        winner = judge.get("round_winner", "tie")
        badge_cls = {"defense": "badge-defense", "prosecution": "badge-prosecution"}.get(winner, "badge-tie")
        badge_label = winner.upper()

        st.markdown(f"""
        <div class="agent-card judge-card">
            <div class="agent-label" style="color:#f0c96b">{tr("judges_ruling")} — {tr("round")} {rn}</div>
            <div style="margin-bottom:0.6rem">
                <span class="score-pill score-defense">{tr("defense")}: {d_score}/10</span>&nbsp;
                <span class="score-pill score-prosecution">{tr("prosecution")}: {p_score}/10</span>&nbsp;
                <span class="winner-badge {badge_cls}">{tr("round_winner")}: {badge_label}</span>
            </div>
            <div style="margin-bottom:0.4rem"><strong>{tr("defense_strengths")}:</strong> {judge.get("defense_strengths", "—")}</div>
            <div style="margin-bottom:0.4rem"><strong>{tr("defense_weaknesses")}:</strong> {judge.get("defense_weaknesses", "—")}</div>
            <div style="margin-bottom:0.4rem"><strong>{tr("reasoning")}:</strong> {judge.get("reasoning", "—")}</div>
        </div>
        """, unsafe_allow_html=True)

    # Current round
    current_round_num = state["current_round"]

    if phase["status"] == "awaiting_choice":
        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {current_round_num} - {tr("your_turn")}</div>', unsafe_allow_html=True)

        # Show opponent's attack
        st.markdown(f"""
        <div class="agent-card opponent-card">
            <div class="agent-label" style="color:#c0392b">{tr("opposing_attack")}</div>
            {phase['opponent_attack']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(tr("choose_strategy"))

        # Display all options in columns
        cols = st.columns(3)

        for idx, opt in enumerate(phase['options']):
            with cols[idx]:
                is_selected = st.session_state.get(f"selected_opt_{current_round_num}", None) == opt['id']
                card_style = "option-card selected" if is_selected else "option-card"

                st.markdown(f"""
                <div class="{card_style}">
                    <div class="option-title">{tr("option")} {opt['id']}: {opt['title']}</div>
                    <div class="option-body">{opt['argument']}</div>
                    <div class="option-strength">{tr("strength")}: {opt['strength']}</div>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"{tr('select_option')} {opt['id']}", key=f"select_opt_{opt['id']}_r{current_round_num}", use_container_width=True):
                    st.session_state[f"selected_opt_{current_round_num}"] = opt['id']


        selected_option_id = st.session_state.get(f"selected_opt_{current_round_num}", None)

        if selected_option_id is None:
            st.info(tr("please_select_strategy"))
            selected_opt = None
        else:
            selected_opt = next(opt for opt in phase['options'] if opt['id'] == selected_option_id)

        # Show evidence request if needed
        evidence_files = None
        if phase.get('needs_evidence'):
            st.markdown(tr("evidence_required"))
            st.info(f"💡 {phase.get('evidence_reason', tr('evidence_reason_default'))}")

            evidence_files = st.file_uploader(
                tr("upload_evidence"),
                type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
                accept_multiple_files=True,
                key="evidence_uploader"
            )

        # Buttons row
        col_proceed, col_end = st.columns([3, 1])

        with col_proceed:
            proceed_disabled = selected_option_id is None
            if st.button(tr("proceed_argument"), key="proceed_btn", disabled=proceed_disabled):
                loader_slot = st.empty()
                loader_slot.markdown(
                    hearing_loader_markup(
                        tr("loader_round_title"),
                        tr("spinner_process_argument"),
                    ),
                    unsafe_allow_html=True,
                )
                time.sleep(0.06)
                try:
                    round_result = run_interactive_round(
                        state,
                        selected_option_id=selected_option_id,
                        evidence_files=evidence_files,
                    )
                    if round_result["status"] == "awaiting_evidence":
                        st.session_state.round_phase = round_result
                    elif round_result["status"] == "checking_credibility":
                        st.session_state.round_phase = round_result
                    elif round_result["status"] == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result
                except Exception as e:
                    st.error(f"{tr('error_processing_round')}: {str(e)}")
                finally:
                    loader_slot.empty()

        with col_end:
            st.markdown('<div class="end-hearing-btn">', unsafe_allow_html=True)
            if st.button(tr("end_hearing"), key="end_hearing_btn"):
                # End the simulation and show final verdict
                st.session_state.round_phase = {"status": "simulation_complete"}

            st.markdown('</div>', unsafe_allow_html=True)

    elif phase["status"] == "checking_credibility":
        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {current_round_num} - {tr("cred_check")}</div>', unsafe_allow_html=True)

        st.markdown(tr("ai_evidence_analysis_complete"))
        st.info(tr("evidence_analysis_info"))

        credibility_reports = phase.get("credibility_reports", [])

        for i, report in enumerate(credibility_reports):
            score = report.get("credibility_score", 5)

            # Determine score class
            if score >= 7:
                score_class = "score-high"
                card_class = "credibility-high"
            elif score >= 4:
                score_class = "score-medium"
                card_class = "credibility-medium"
            else:
                score_class = "score-low"
                card_class = "credibility-low"

            # Document header
            st.markdown(f"""
            <div class="credibility-card {card_class}">
                <div class="agent-label" style="color:#3498db">{tr("evidence_document")} {i+1}</div>
                <div style="margin-bottom:1rem">
                    <span class="credibility-score {score_class}">{tr("credibility_score")}: {score}/10</span>
                </div>
            """, unsafe_allow_html=True)

            # Display fields using streamlit components to avoid HTML rendering issues
            st.markdown(f"**{tr('relevance')}:** {report.get('relevance', 'N/A')}")
            st.markdown(f"**{tr('authenticity_concerns')}:** {report.get('authenticity_concerns', 'N/A')}")
            st.markdown(f"**{tr('admissibility_issues')}:** {report.get('admissibility_issues', 'N/A')}")
            st.markdown(f"**{tr('strategic_value')}:** {report.get('strategic_value', 'N/A')}")

            # Red flags
            red_flags = report.get("red_flags", [])
            if red_flags:
                st.markdown(f"**{tr('red_flags_identified')}:**")
                for flag in red_flags:
                    st.markdown(f'<div class="red-flag-item">⚠️ {flag}</div>', unsafe_allow_html=True)

            st.markdown(f"**{tr('recommendations')}:** {report.get('recommendations', 'N/A')}")
            st.markdown("---")
            st.markdown(f"*{tr('overall_assessment')}:* {report.get('overall_assessment', 'N/A')}")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Two buttons: Skip or Use Evidence
        col_skip, col_use = st.columns(2)

        with col_skip:
            if st.button(tr("skip_evidence"), key="skip_after_cred"):
                with st.spinner(tr("spinner_without_evidence")):
                    # Clear credibility state and proceed without evidence
            
                    if "credibility_reports" in state:
                        del state["credibility_reports"]
                    if "evidence_texts" in state:
                        del state["evidence_texts"]

                    # Re-run the round without evidence
                    round_result = run_interactive_round(state)

                    if round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])

                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result



        with col_use:
            if st.button(tr("use_this_evidence"), key="use_evidence"):
                with st.spinner(tr("spinner_incorporate")):
                    # Proceed with evidence
                    round_result = run_interactive_round(state)

                    if round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])

                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result



    elif phase["status"] == "awaiting_evidence":
        st.markdown(f'<div class="round-header">⚔️ {tr("round")} {current_round_num} - {tr("evidence_needed")}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="evidence-box">
            <h3 style="color:#f0c96b; margin-bottom:1rem">{tr("evidence_request")}</h3>
            <p>{phase.get('reason', tr('evidence_request_default'))}</p>
        </div>
        """, unsafe_allow_html=True)

        evidence_files = st.file_uploader(
            tr("upload_evidence"),
            type=['pdf', 'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'tif'],
            accept_multiple_files=True,
            key="evidence_uploader_2"
        )

        col_skip, col_submit = st.columns(2)

        with col_skip:
            if st.button(tr("skip_evidence"), key="skip_evidence"):
                with st.spinner(tr("spinner_without_evidence")):
                    round_result = run_interactive_round(state, evidence_files=None)

                    if round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])

                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result



        with col_submit:
            if st.button(tr("submit_evidence_analysis"), key="submit_evidence") and evidence_files:
                with st.spinner(tr("spinner_analyze_evidence")):
                    round_result = run_interactive_round(state, evidence_files=evidence_files)

                    if round_result["status"] == "checking_credibility":
                        st.session_state.round_phase = round_result

                    elif round_result.get("status") == "round_complete":
                        st.session_state.completed_rounds.append(round_result["round_data"])

                        # Continue to next round
                        next_round_result = run_interactive_round(state)
                        st.session_state.round_phase = next_round_result



    elif phase["status"] == "simulation_complete":
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.success(tr("hearing_complete"))

        # Calculate final verdict
        final = compute_win_probability(state["round_results"], language)
        win_prob = final["win_probability"]

        st.markdown(f'<div class="final-title">{tr("final_verdict")}</div>', unsafe_allow_html=True)

        # Win probability bar
        st.markdown(f"**{tr('win_probability_defense')}**")
        marker_left = max(2, min(97, win_prob))
        st.markdown(f"""
        <div class="win-probability-bar">
            <div class="win-marker" style="left:{marker_left}%"></div>
        </div>
        <div style="display:flex; justify-content:space-between; font-size:0.8rem; color:#8a8577; margin-bottom:0.8rem">
            <span>0% ({tr('lose')})</span>
            <span style="font-size:1.2rem; font-weight:700; color:{'#27ae60' if win_prob >= 55 else '#c0392b' if win_prob < 45 else '#f0c96b'}">{win_prob}%</span>
            <span>100% ({tr('win')})</span>
        </div>
        """, unsafe_allow_html=True)

        col_s, col_w, col_sg = st.columns(3)

        with col_s:
            st.markdown(f"**{tr('strong_points')}**")
            for pt in final.get("strong_points", []):
                if pt:
                    st.markdown(f"<div class='point-item'><span style='color:#27ae60'>▸</span> {pt}</div>", unsafe_allow_html=True)

        with col_w:
            st.markdown(f"**{tr('weak_points')}**")
            for pt in final.get("weak_points", []):
                if pt:
                    st.markdown(f"<div class='point-item'><span style='color:#e67e22'>▸</span> {pt}</div>", unsafe_allow_html=True)

        with col_sg:
            st.markdown(f"**{tr('strategy_suggestions')}**")
            for sug in final.get("suggestions", []):
                if sug:
                    st.markdown(f"<div class='point-item'><span style='color:#f0c96b'>▸</span> {sug}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(tr("start_new_hearing")):
            reset_simulation()
            st.rerun()
