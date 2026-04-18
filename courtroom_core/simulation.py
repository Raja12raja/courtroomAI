"""Orchestrate interactive and batch courtroom simulations."""
from courtroom_core.agents import (
    judge_ai,
    lawyer_ai,
    lawyer_ai_with_evidence,
    lawyer_ai_with_options,
    opponent_ai,
)
from courtroom_core.credibility import check_evidence_credibility
from courtroom_core.documents import process_evidence_file
from courtroom_core.rag import search
from courtroom_core.scoring import compute_win_probability

def run_simulation(case_description: str, num_rounds: int = 2, language: str = "en") -> dict:
    """
    Orchestrates the full courtroom simulation (non-interactive version).
    Returns all round data + final verdict.
    """
    context = search(case_description)
    history = []
    round_results = []
    rounds_data = []

    current_argument = case_description

    for round_num in range(1, num_rounds + 1):
        opp = opponent_ai(current_argument, context, history, language)
        law = lawyer_ai(current_argument, context, history, language)
        verdict = judge_ai(current_argument, law, opp, round_num, credibility_reports=None, language=language)

        history.append({"opponent": opp, "lawyer": law})
        round_results.append(verdict)
        rounds_data.append({
            "round": round_num,
            "opponent": opp,
            "lawyer": law,
            "judge": verdict
        })

        # Next round argues from lawyer's improved position
        current_argument = law

    final = compute_win_probability(round_results, language)

    return {
        "rounds": rounds_data,
        "final": final,
        "context_used": context[:400] + "..."
    }


def start_interactive_simulation(case_description: str, language: str = "en") -> dict:
    """
    Initializes an interactive simulation session.
    Returns context and initial state.
    Simulation runs continuously until user ends it.
    """
    context = search(case_description)
    return {
        "context": context,
        "current_round": 1,
        "history": [],
        "round_results": [],
        "current_argument": case_description,
        "case_description": case_description,  # Store for credibility checks
        "language": language  # Store language preference
    }


def run_interactive_round(
    state: dict,
    selected_option_id: int = None,
    evidence_files: list = None
) -> dict:
    """
    Runs one round of the interactive simulation.
    
    Returns:
    - If waiting for user choice: {"status": "awaiting_choice", "options": [...], "opponent_attack": "..."}
    - If checking credibility: {"status": "checking_credibility", "credibility_reports": [...]}
    - If round complete: {"status": "round_complete", "round_data": {...}}
    """
    context = state["context"]
    history = state["history"]
    current_round = state["current_round"]
    current_argument = state["current_argument"]
    case_description = state.get("case_description", current_argument)
    language = state.get("language", "en")
    
    # Step 1: Generate opponent attack if not yet done
    if "pending_opponent" not in state:
        opp = opponent_ai(current_argument, context, history, language)
        state["pending_opponent"] = opp
        
        # Step 2: Generate lawyer options
        options_data = lawyer_ai_with_options(current_argument, context, history, opp, language)
        state["pending_options"] = options_data
        
        return {
            "status": "awaiting_choice",
            "opponent_attack": opp,
            "options": options_data["options"],
            "needs_evidence": options_data["needs_evidence"],
            "evidence_reason": options_data.get("evidence_reason", "")
        }
    
    # Step 3: User has selected an option (or we have selected_argument from previous call)
    if (selected_option_id is not None or "selected_argument" in state) and "final_lawyer_response" not in state:
        # Get or retrieve selected argument
        if "selected_argument" not in state:
            options_data = state["pending_options"]
            selected = next((opt for opt in options_data["options"] if opt["id"] == selected_option_id), None)
            
            if not selected:
                selected = options_data["options"][0]  # Fallback
            
            state["selected_argument"] = selected["argument"]
        
        # Step 4: If evidence provided, perform credibility check
        if evidence_files and "credibility_reports" not in state:
            evidence_texts = []
            credibility_reports = []
            
            for f in evidence_files:
                # Reset file pointer
                f.seek(0)
                
                # Process file based on type (PDF or image)
                txt = process_evidence_file(f, language)
                evidence_texts.append(txt)
                
                # Perform credibility check
                cred_report = check_evidence_credibility(txt, case_description, context, language)
                credibility_reports.append(cred_report)
            
            state["evidence_texts"] = evidence_texts
            state["credibility_reports"] = credibility_reports
            
            return {
                "status": "checking_credibility",
                "credibility_reports": credibility_reports,
                "evidence_texts": evidence_texts
            }
        
        # Step 5: Generate final lawyer response with or without evidence
        credibility_reports_for_judge = None
        
        if "credibility_reports" in state and "evidence_texts" in state:
            # User has reviewed credibility - proceed with evidence
            law = lawyer_ai_with_evidence(
                state["selected_argument"],
                context,
                history,
                state["evidence_texts"],
                state["credibility_reports"],
                language
            )
            credibility_reports_for_judge = state["credibility_reports"]
            
        elif evidence_files:
            # Evidence provided but credibility not checked yet (shouldn't happen)
            evidence_texts = [process_evidence_file(f, language) for f in evidence_files]
            credibility_reports = [
                check_evidence_credibility(txt, case_description, context, language)
                for txt in evidence_texts
            ]
            law = lawyer_ai_with_evidence(
                state["selected_argument"],
                context,
                history,
                evidence_texts,
                credibility_reports,
                language
            )
            credibility_reports_for_judge = credibility_reports
        else:
            # No evidence - use selected argument directly
            law = state["selected_argument"]
            credibility_reports_for_judge = None
        
        state["final_lawyer_response"] = law
        opp = state["pending_opponent"]
        
        # Judge evaluation - NOW INCLUDES CREDIBILITY REPORTS
        verdict = judge_ai(current_argument, law, opp, current_round, credibility_reports=credibility_reports_for_judge, language=language)
        
        # Update state
        history.append({"opponent": opp, "lawyer": law})
        state["round_results"].append(verdict)
        
        round_data = {
            "round": current_round,
            "opponent": opp,
            "lawyer": law,
            "judge": verdict
        }
        
        # Prepare for next round
        state["current_argument"] = law
        state["current_round"] += 1
        state["history"] = history
        
        # Clean up temporary state
        del state["pending_opponent"]
        del state["pending_options"]
        del state["final_lawyer_response"]
        if "selected_argument" in state:
            del state["selected_argument"]
        if "evidence_texts" in state:
            del state["evidence_texts"]
        if "credibility_reports" in state:
            del state["credibility_reports"]
        
        # Round is complete - continuous mode (no round limit)
        return {
            "status": "round_complete",
            "round_data": round_data
        }
    
    # Should not reach here in normal flow
    return {"status": "error", "message": "Invalid state"}
