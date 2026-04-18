"""LLM-based evidence credibility scoring."""
import json
import re

from courtroom_core.llm import ask_llm
from courtroom_core.locales import get_language_instruction, get_translation

def check_evidence_credibility(evidence_text: str, case_description: str, context: str, language: str = "en") -> dict:
    """
    Performs credibility check on uploaded evidence.
    Analyzes relevance, authenticity concerns, and strategic value.
    Returns dict with credibility score, issues, and recommendations.
    """
    # Detect if this is image evidence (contains OCR/Vision markers)
    is_image_evidence = any([
        "OCR" in evidence_text,
        get_translation("ocr_extracted", language) in evidence_text,
        get_translation("visual_analysis", language) in evidence_text
    ])
    
    lang_instruction = get_language_instruction(language)
    
    evidence_type_note = ""
    if is_image_evidence:
        evidence_type_note = f"""
NOTE: This is IMAGE EVIDENCE containing both OCR text extraction and visual content analysis.
Evaluate both the textual content AND the visual scene description.
Consider image quality, clarity, and forensic authenticity indicators."""
    
    system = f"""You are an experienced legal evidence analyst in Indian courts. 
You evaluate documentary evidence for authenticity, relevance, and strategic value. 
You identify potential credibility issues, contradictions, and procedural concerns. 
IMPORTANT: The credibility score MUST reflect the severity of any red flags you identify. 
Each significant red flag should reduce the score by 2-3 points from a baseline of 8-9.{lang_instruction}"""

    prompt = f"""
CASE DESCRIPTION:
{case_description[:500]}

LEGAL CONTEXT:
{context[:400]}

EVIDENCE CONTENT:
{evidence_text[:2000]}
{evidence_type_note}

Your task:
Perform a thorough credibility check on this evidence. Analyze:

1. **Relevance**: How directly does this evidence relate to the case?
2. **Authenticity Concerns**: Any signs of potential tampering, inconsistencies, or missing authentication?
3. **Legal Admissibility**: Procedural issues that might affect admissibility in court?
4. **Strategic Value**: How strong is this evidence for the defense?
5. **Red Flags**: Any contradictions with the case narrative or potential prosecution attacks?
6. **Recommendations**: How should this evidence be used (or not used)?

SCORING GUIDELINES:
- Start with baseline 8-9 for clean, relevant evidence
- Deduct 2-3 points for EACH major red flag (tampering signs, contradictions, quality issues)
- Deduct 1-2 points for EACH moderate concern (missing authentication, procedural issues)
- Score 1-3: Highly questionable, should NOT be used
- Score 4-6: Significant concerns, use with caution
- Score 7-8: Minor concerns, generally reliable
- Score 9-10: Highly credible, strong evidence

Respond in this EXACT JSON format:
{{
  "credibility_score": <integer 1-10 based on red flags identified>,
  "relevance": "<brief assessment>",
  "authenticity_concerns": "<list concerns or 'None identified'>",
  "admissibility_issues": "<list issues or 'None identified'>",
  "strategic_value": "<brief assessment>",
  "red_flags": ["<flag 1>", "<flag 2>", ...] or [],
  "recommendations": "<how to use this evidence effectively>",
  "overall_assessment": "<2-3 sentence summary>"
}}

CRITICAL: Ensure credibility_score is proportional to red_flags. More red flags = lower score.
Return ONLY valid JSON. No extra text.
"""
    raw = ask_llm(prompt, system, language)

    try:
        cleaned = re.sub(r"```(?:json)?|```", "", raw).strip()
        result = json.loads(cleaned)
        
        # Validate that score makes sense with red flags
        num_red_flags = len(result.get("red_flags", []))
        score = result.get("credibility_score", 5)
        
        # If there are 2+ red flags but score is still high, adjust it
        if num_red_flags >= 2 and score > 6:
            result["credibility_score"] = max(3, 7 - (num_red_flags * 2))
        elif num_red_flags == 1 and score > 7:
            result["credibility_score"] = 6
        
        return result
        
    except json.JSONDecodeError as e:
        # Log the actual response for debugging
        print(f"JSON Decode Error: {e}")
        print(f"Raw LLM response: {raw[:500]}")
        
        # Fallback structure
        return {
            "credibility_score": 5,
            "relevance": "Unable to fully analyze",
            "authenticity_concerns": "Analysis incomplete",
            "admissibility_issues": "Requires manual review",
            "strategic_value": "Uncertain",
            "red_flags": [],
            "recommendations": "Consult with legal expert before using this evidence.",
            "overall_assessment": "Credibility analysis could not be completed. Manual review recommended."
        }
