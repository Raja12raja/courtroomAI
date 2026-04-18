"""Post-hearing win probability from judge round results."""
import json
import math

from courtroom_core.llm import ask_llm
from courtroom_core.locales import get_language_instruction, get_translation

def sigmoid(x):
    """
    Sigmoid function to convert score differential to probability.
    Maps [-infinity, +infinity] to [0, 1] in an S-curve.
    """
    return 1 / (1 + math.exp(-x))


def compute_win_probability(round_results: list, language: str = "en") -> dict:
    """
    Compute final win probability from judge scores across all rounds.
    Uses a sophisticated algorithm that considers:
    1. Round winners (who won more rounds) - adjusted for narrow margins
    2. Score differentials (margin of victory)
    3. Recent performance (later rounds weighted more)
    4. Overall momentum
    5. Evidence quality impact across rounds
    
    Also generates final strengths, weaknesses, and strategy suggestions.
    """
    if not round_results:
        return {
            "win_probability": 50,
            "strong_points": [],
            "weak_points": [],
            "suggestions": [],
            "detailed_breakdown": {
                "rounds_won": {"defense": 0, "prosecution": 0},
                "total_scores": {"defense": 0, "prosecution": 0},
                "average_margin": 0,
                "momentum": "neutral",
                "evidence_quality": "unknown"
            }
        }

    num_rounds = len(round_results)
    
    # Calculate basic statistics
    defense_rounds_won = sum(1 for r in round_results if r.get("round_winner") == "defense")
    prosecution_rounds_won = sum(1 for r in round_results if r.get("round_winner") == "prosecution")
    ties = sum(1 for r in round_results if r.get("round_winner") not in ["defense", "prosecution"])
    
    total_defense = sum(r.get("defense_score", 5) for r in round_results)
    total_prosecution = sum(r.get("prosecution_score", 5) for r in round_results)
    
    # Calculate average scores and margin
    avg_defense = total_defense / num_rounds
    avg_prosecution = total_prosecution / num_rounds
    avg_margin = avg_defense - avg_prosecution
    
    # Analyze evidence quality impact
    evidence_rounds = [r for r in round_results if r.get("evidence_impact") and r.get("evidence_impact") != "N/A"]
    if evidence_rounds:
        evidence_quality = "evidence_used"
    else:
        evidence_quality = "no_evidence"
    
    # Component 1: Round Win Percentage with Margin Adjustment (30% weight)
    # Reduce the impact of narrow victories
    if defense_rounds_won + prosecution_rounds_won > 0:
        raw_round_win = defense_rounds_won / (defense_rounds_won + prosecution_rounds_won)
        
        # Adjust based on how narrow the wins were
        # If average margin is small (< 1.5), reduce the round win impact
        if abs(avg_margin) < 1.5:
            # Narrow victories - move closer to 0.5
            round_win_factor = 0.5 + (raw_round_win - 0.5) * 0.5
        else:
            round_win_factor = raw_round_win
    else:
        round_win_factor = 0.5
    
    # Component 2: Score-Based Probability (45% weight)
    # Primary component - directly based on score differential
    # Use a more sensitive sigmoid that responds better to score differences
    # Dividing by 2.5 instead of 3 makes it more responsive
    score_diff = avg_margin
    score_factor = sigmoid(score_diff / 2.5)
    
    # Component 3: Consistency Factor (15% weight)
    # Rewards consistent performance across rounds
    defense_margins = []
    for r in round_results:
        margin = r.get("defense_score", 5) - r.get("prosecution_score", 5)
        defense_margins.append(margin)
    
    # Standard deviation of margins (lower = more consistent)
    if len(defense_margins) > 1:
        mean_margin = sum(defense_margins) / len(defense_margins)
        variance = sum((m - mean_margin) ** 2 for m in defense_margins) / len(defense_margins)
        std_dev = math.sqrt(variance)
        
        # Higher consistency = lower std dev = higher factor
        # Normalize: std_dev of 0 = 1.0, std_dev of 3+ = 0.5
        consistency_factor = max(0.5, 1.0 - (std_dev / 6))
        
        # Apply the mean margin direction
        if mean_margin > 0:
            consistency_factor = 0.5 + (consistency_factor - 0.5)
        else:
            consistency_factor = 0.5 - (consistency_factor - 0.5)
    else:
        # Single round - base on that round's margin
        consistency_factor = sigmoid(defense_margins[0] / 3)
    
    # Component 4: Momentum (10% weight)
    # Check if defense is improving over time
    if num_rounds >= 2:
        first_half = round_results[:num_rounds//2]
        second_half = round_results[num_rounds//2:]
        
        first_half_avg = sum(r.get("defense_score", 5) - r.get("prosecution_score", 5) for r in first_half) / len(first_half)
        second_half_avg = sum(r.get("defense_score", 5) - r.get("prosecution_score", 5) for r in second_half) / len(second_half)
        
        momentum_diff = second_half_avg - first_half_avg
        # Positive momentum boosts, negative momentum reduces
        momentum_factor = 0.5 + (momentum_diff / 10)
        momentum_factor = max(0, min(1, momentum_factor))
        
        if momentum_diff > 1:
            momentum_label = "improving"
        elif momentum_diff < -1:
            momentum_label = "declining"
        else:
            momentum_label = "stable"
    else:
        momentum_factor = 0.5
        momentum_label = "insufficient_data"
    
    # Combine all components with adjusted weights
    # Score factor has the highest weight since it's most directly related to performance
    win_probability = (
        round_win_factor * 0.30 +    # Reduced from 35% to 30%
        score_factor * 0.45 +          # Increased from 35% to 45%
        consistency_factor * 0.15 +    # New component
        momentum_factor * 0.10
    ) * 100
    
    # Clamp to reasonable bounds (never show 0% or 100%)
    win_probability = max(5, min(95, win_probability))
    win_probability = round(win_probability)
    
    # Extract strengths and weaknesses
    strong_points = [r["defense_strengths"] for r in round_results if r.get("defense_strengths")]
    weak_points = [r["defense_weaknesses"] for r in round_results if r.get("defense_weaknesses")]
    
    lang_instruction = get_language_instruction(language)
    
    # Generate strategy suggestions using LLM
    evidence_context = ""
    if evidence_rounds:
        evidence_context = f"\n- Evidence was used in {len(evidence_rounds)}/{num_rounds} rounds"
    
    defense = get_translation("defense", language)
    prosecution = get_translation("prosecution", language)
    
    summary_prompt = f"""
Based on this courtroom simulation analysis:
- {defense} rounds won: {defense_rounds_won}/{num_rounds}
- {prosecution} rounds won: {prosecution_rounds_won}/{num_rounds}
- {defense} average score: {avg_defense:.1f}
- {prosecution} average score: {avg_prosecution:.1f}
- Average margin: {avg_margin:.1f} points per round
- Performance momentum: {momentum_label}{evidence_context}
- Current win probability: {win_probability}%

Key weaknesses identified across rounds:
{'; '.join(weak_points) if weak_points else 'None identified'}

Give 3-4 concrete, actionable legal strategy suggestions to improve the defense case.
Focus on addressing the weaknesses and building on strengths.
If evidence quality was an issue, suggest how to obtain better evidence.
Format as a JSON array of strings. Return ONLY the JSON array.{lang_instruction}
"""
    raw_suggestions = ask_llm(summary_prompt, language=language)
    try:
        cleaned = extract_json_from_text(raw_suggestions)
        suggestions = json.loads(cleaned)
        if not isinstance(suggestions, list):
            suggestions = [str(suggestions)]
    except Exception:
        suggestions = [
            "Review and strengthen evidence documentation.",
            "Prepare stronger witness statements.",
            "Research applicable BNS 2023 sections.",
            "Address procedural weaknesses identified by prosecution."
        ]

    return {
        "win_probability": win_probability,
        "strong_points": strong_points,
        "weak_points": weak_points,
        "suggestions": suggestions,
        "detailed_breakdown": {
            "rounds_won": {
                "defense": defense_rounds_won,
                "prosecution": prosecution_rounds_won,
                "ties": ties
            },
            "total_scores": {
                "defense": total_defense,
                "prosecution": total_prosecution
            },
            "average_scores": {
                "defense": round(avg_defense, 1),
                "prosecution": round(avg_prosecution, 1)
            },
            "average_margin": round(avg_margin, 1),
            "momentum": momentum_label,
            "evidence_quality": evidence_quality,
            "component_contributions": {
                "round_wins_adjusted": f"{round(round_win_factor * 30, 1)}%",
                "score_based": f"{round(score_factor * 45, 1)}%",
                "consistency": f"{round(consistency_factor * 15, 1)}%",
                "momentum": f"{round(momentum_factor * 10, 1)}%"
            }
        }
    }
