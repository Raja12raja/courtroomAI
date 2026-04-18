"""Adversarial courtroom agents: defense, prosecution, judge."""
import json

from courtroom_core.json_utils import extract_json_from_text
from courtroom_core.llm import ask_llm
from courtroom_core.locales import get_language_instruction, get_translation

def lawyer_ai_with_options(user_argument: str, context: str, history: list, opponent_attack: str = "", language: str = "en") -> dict:
    """
    Defense Lawyer AI — generates multiple argument strategy options for user to choose from.
    Returns dict with 3 options and whether evidence is needed.
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] Opponent said: {r['opponent']}\nPrevious Lawyer response: {r['lawyer']}\n"

    opponent_context = f"\n\nOPPONENT'S LATEST ATTACK:\n{opponent_attack}" if opponent_attack else ""
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an experienced defense lawyer in an Indian court. 
You cite relevant sections from BNS 2023 and IPC where applicable. 
Be precise, strategic, and legally sound.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ROUNDS:
{history_text if history_text else "This is the first round."}

CURRENT USER ARGUMENT:
{user_argument}
{opponent_context}

Your task:
Generate 3 different defense strategy options for the user to choose from.

Each option should:
1. Take a different legal angle (e.g., evidence-based, procedural, constitutional rights)
2. Be specific and actionable
3. Reference relevant BNS 2023 or IPC sections
4. Be under 150 words

Also, determine if additional evidence documents would significantly strengthen any argument.

Respond in this EXACT JSON format:
{{
  "needs_evidence": true or false,
  "evidence_reason": "<brief explanation if true, otherwise empty string>",
  "options": [
    {{
      "id": 1,
      "title": "<Short strategy title>",
      "argument": "<Full argument text>",
      "strength": "<Why this approach is strong>"
    }},
    {{
      "id": 2,
      "title": "<Short strategy title>",
      "argument": "<Full argument text>",
      "strength": "<Why this approach is strong>"
    }},
    {{
      "id": 3,
      "title": "<Short strategy title>",
      "argument": "<Full argument text>",
      "strength": "<Why this approach is strong>"
    }}
  ]
}}

Return ONLY valid JSON.
"""
    raw = ask_llm(prompt, system, language)

    try:
        cleaned = extract_json_from_text(raw)
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fallback structure
        return {
            "needs_evidence": False,
            "evidence_reason": "",
            "options": [
                {
                    "id": 1,
                    "title": "Direct Defense",
                    "argument": user_argument,
                    "strength": "Straightforward approach based on user's input."
                }
            ]
        }


def lawyer_ai_with_evidence(
    selected_argument: str,
    context: str,
    history: list,
    evidence_texts: list,
    credibility_reports: list,
    language: str = "en"
) -> str:
    """
    Defense Lawyer AI — strengthens the selected argument using uploaded evidence
    and incorporating credibility assessments.
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] Opponent said: {r['opponent']}\nPrevious Lawyer response: {r['lawyer']}\n"

    evidence_summary = ""
    for i, (txt, cred_report) in enumerate(zip(evidence_texts, credibility_reports)):
        evidence_doc = get_translation("evidence_doc", language)
        cred_score = get_translation("credibility_score", language)
        relevance = get_translation("relevance", language)
        red_flags = get_translation("red_flags", language)
        none = get_translation("none", language)
        recommendations = get_translation("recommendations", language)
        
        evidence_summary += f"\n\n[{evidence_doc} {i+1}]:\n"
        evidence_summary += f"Content: {txt[:800]}\n"
        evidence_summary += f"{cred_score}: {cred_report['credibility_score']}/10\n"
        evidence_summary += f"{relevance}: {cred_report['relevance']}\n"
        evidence_summary += f"{red_flags}: {', '.join(cred_report['red_flags']) if cred_report['red_flags'] else none}\n"
        evidence_summary += f"{recommendations}: {cred_report['recommendations']}\n"
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an experienced defense lawyer in an Indian court. 
You cite relevant sections from BNS 2023 and IPC where applicable. 
Incorporate evidence intelligently, address any credibility concerns preemptively, 
and use only the strongest parts of the evidence.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ROUNDS:
{history_text if history_text else "This is the first round."}

UPLOADED EVIDENCE (with credibility analysis):
{evidence_summary}

SELECTED ARGUMENT STRATEGY:
{selected_argument}

Your task:
Strengthen the selected argument by:
1. Incorporating specific facts/details from the uploaded evidence
2. Addressing any credibility concerns proactively
3. Using only evidence with high credibility scores strategically
4. Avoiding or downplaying evidence with red flags
5. Citing relevant legal sections from BNS 2023/IPC
6. Preemptively countering opposition attacks on evidence authenticity
7. Keeping response under 200 words, structured and persuasive

Respond as the defense lawyer now:
"""
    return ask_llm(prompt, system, language)


def lawyer_ai(user_argument: str, context: str, history: list, language: str = "en") -> str:
    """
    Defense Lawyer AI — strengthens the user's argument using legal context
    and prior round history. (Original non-interactive version for fallback)
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] Opponent said: {r['opponent']}\nPrevious Lawyer response: {r['lawyer']}\n"
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an experienced defense lawyer in an Indian court. 
You cite relevant sections from BNS 2023 and IPC where applicable. 
Be precise, strategic, and legally sound. Do NOT repeat yourself.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ROUNDS:
{history_text if history_text else "This is the first round."}

CURRENT USER ARGUMENT:
{user_argument}

Your task:
1. Identify the strongest legal points in the user's argument.
2. Strengthen weak points using the legal context above.
3. Preemptively counter any likely opposition attacks.
4. Keep your response under 200 words, structured and persuasive.

Respond as the defense lawyer now:
"""
    return ask_llm(prompt, system, language)


def opponent_ai(user_argument: str, context: str, history: list, language: str = "en") -> str:
    """
    Opposing Counsel AI — attacks the user's argument, finds loopholes,
    challenges evidence using legal context.
    """
    history_text = ""
    for i, r in enumerate(history):
        round_label = get_translation("round", language)
        history_text += f"\n[{round_label} {i+1}] You previously attacked: {r['opponent']}\n"
    
    lang_instruction = get_language_instruction(language)

    system = f"""You are an aggressive opposing counsel in an Indian court. 
You exploit legal loopholes, challenge evidence credibility, 
and reference procedural weaknesses. Be sharp and adversarial. 
Do NOT repeat prior attacks.{lang_instruction}"""

    prompt = f"""
LEGAL CONTEXT (from case documents):
{context}

PRIOR ATTACKS (avoid repeating):
{history_text if history_text else "This is the first round."}

ARGUMENT TO ATTACK:
{user_argument}

Your task:
1. Identify the 2-3 biggest weaknesses or contradictions.
2. Challenge the evidence or witness credibility if applicable.
3. Raise procedural or legal objections using the context above.
4. Keep your response under 200 words. Be aggressive but professional.

Respond as the opposing counsel now:
"""
    return ask_llm(prompt, system, language)


def judge_ai(user_argument: str, lawyer_arg: str, opponent_arg: str, round_num: int, credibility_reports: list = None, language: str = "en") -> dict:
    """
    Judge AI — evaluates both sides, gives scores and structured reasoning.
    Now considers evidence credibility scores in evaluation.
    Returns a dict with scores and analysis.
    """
    lang_instruction = get_language_instruction(language)
    
    system = f"""You are a neutral, senior judge in an Indian court. 
You evaluate arguments on: legal soundness, evidence use, clarity, and persuasiveness. 
You are fair, objective, and concise. 
When evidence is presented, you MUST consider its credibility score and red flags in your scoring. 
Low-credibility evidence (score < 6) should significantly reduce the argument's score. 
CRITICAL: You MUST return ONLY valid JSON with no additional text before or after.{lang_instruction}"""

    # Build evidence credibility section if reports are provided
    evidence_section = ""
    if credibility_reports and len(credibility_reports) > 0:
        evidence_doc = get_translation("evidence_doc", language)
        cred_score = get_translation("credibility_score", language)
        red_flags = get_translation("red_flags", language)
        none = get_translation("none", language)
        
        evidence_section = f"\n\nEVIDENCE CREDIBILITY ANALYSIS ({get_translation('defense', language)}):\n"
        for i, report in enumerate(credibility_reports):
            score = report.get("credibility_score", 5)
            flags = report.get("red_flags", [])
            concerns = report.get("authenticity_concerns", "Unknown")
            
            evidence_section += f"\n[{evidence_doc} {i+1}]:\n"
            evidence_section += f"- {cred_score}: {score}/10\n"
            evidence_section += f"- {red_flags}: {', '.join(flags) if flags else none}\n"
            evidence_section += f"- Authenticity Concerns: {concerns}\n"
            evidence_section += f"- Overall: {report.get('overall_assessment', 'N/A')}\n"
        
        evidence_section += "\n⚠️ SCORING GUIDANCE:\n"
        evidence_section += "- Evidence with score 7-10: Strong support, minimal deduction\n"
        evidence_section += "- Evidence with score 4-6: Moderate concerns, deduct 1-2 points from defense\n"
        evidence_section += "- Evidence with score 1-3: Serious issues, deduct 2-4 points from defense\n"
        evidence_section += "- Multiple red flags: Each should further reduce defense score\n"
    
    round_label = get_translation("round", language)
    defense = get_translation("defense", language)
    prosecution = get_translation("prosecution", language)

    prompt = f"""
{round_label.upper()} {round_num} EVALUATION

{defense.upper()} (User + Lawyer AI):
{lawyer_arg}

{prosecution.upper()} (Opponent AI):
{opponent_arg}
{evidence_section}

Your task:
Evaluate this round considering ALL factors including evidence credibility.

CRITICAL EVALUATION RULES:
1. If defense used evidence with credibility score < 6, their score MUST be reduced by 1-3 points
2. If defense evidence has 2+ red flags, their score MUST be reduced by 2-4 points
3. Strong legal arguments cannot fully compensate for weak/questionable evidence
4. Evidence with authenticity concerns undermines the entire defense strategy

Respond ONLY in this exact JSON format (no markdown, no extra text):
{{
  "defense_score": <integer 1-10, ADJUSTED DOWN if evidence has low credibility>,
  "prosecution_score": <integer 1-10>,
  "defense_strengths": "<1-2 sentences>",
  "defense_weaknesses": "<1-2 sentences, MUST mention evidence credibility issues if present>",
  "prosecution_strengths": "<1-2 sentences>",
  "prosecution_weaknesses": "<1-2 sentences>",
  "round_winner": "defense" or "prosecution",
  "reasoning": "<2-3 sentences explaining your scoring, MUST address evidence credibility if reports provided>",
  "evidence_impact": "<1 sentence on how evidence quality affected the scoring, or 'N/A' if no evidence>"
}}

IMPORTANT: Return ONLY the JSON object above. No ```json markers, no explanation, nothing else.
"""
    raw = ask_llm(prompt, system, language)

    # Safely parse JSON from LLM output
    try:
        cleaned = extract_json_from_text(raw)
        result = json.loads(cleaned)
        
        # Additional validation: If evidence was provided with low credibility, ensure defense score reflects it
        if credibility_reports and len(credibility_reports) > 0:
            avg_cred_score = sum(r.get("credibility_score", 5) for r in credibility_reports) / len(credibility_reports)
            total_red_flags = sum(len(r.get("red_flags", [])) for r in credibility_reports)
            
            defense_score = result.get("defense_score", 5)
            
            # Apply automatic deductions if LLM didn't adjust properly
            if avg_cred_score < 6 and defense_score > 6:
                # Low credibility evidence but high defense score - adjust down
                penalty = int((6 - avg_cred_score) * 0.5) + 1
                result["defense_score"] = max(3, defense_score - penalty)
                
            if total_red_flags >= 2 and defense_score > 5:
                # Multiple red flags - additional penalty
                result["defense_score"] = max(3, result["defense_score"] - 1)
        
        # Ensure evidence_impact field exists
        if "evidence_impact" not in result:
            result["evidence_impact"] = "N/A"
        
        return result
        
    except json.JSONDecodeError as e:
        # Enhanced error logging
        print(f"[Judge AI] JSON Decode Error: {e}")
        print(f"[Judge AI] Raw response length: {len(raw)}")
        print(f"[Judge AI] Raw response (first 500 chars): {raw[:500]}")
        print(f"[Judge AI] Cleaned text (first 500 chars): {extract_json_from_text(raw)[:500]}")
        
        return {
            "defense_score": 5,
            "prosecution_score": 5,
            "defense_strengths": "Could not parse judge response - see logs for details.",
            "defense_weaknesses": "JSON parsing failed.",
            "prosecution_strengths": "Unable to evaluate.",
            "prosecution_weaknesses": "Unable to evaluate.",
            "round_winner": "tie",
            "reasoning": f"Error parsing judge response. First 200 chars: {raw[:200]}",
            "evidence_impact": "Unable to evaluate"
        }

