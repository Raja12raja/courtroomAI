"""Extract JSON objects from LLM output (markdown fences, truncation)."""
import re

def extract_json_from_text(text: str) -> str:
    """
    Extract JSON from text that may contain markdown code blocks or other formatting.
    Tries multiple extraction strategies.
    """
    # Strategy 1: Remove markdown code blocks (```json ... ``` or ``` ... ```)
    # Match both opening and closing code blocks
    cleaned = re.sub(r"```(?:json)?\s*", "", text)
    cleaned = re.sub(r"```\s*$", "", cleaned)
    cleaned = cleaned.strip()
    
    # Strategy 2: If that didn't work, try to find JSON object/array boundaries
    if not cleaned.startswith(("{", "[")):
        # Look for first { or [
        start_brace = cleaned.find("{")
        start_bracket = cleaned.find("[")
        
        if start_brace == -1 and start_bracket == -1:
            return text  # No JSON found, return original
        
        if start_brace != -1 and (start_bracket == -1 or start_brace < start_bracket):
            # Found { first
            start = start_brace
            # Find matching closing }
            brace_count = 0
            for i in range(start, len(cleaned)):
                if cleaned[i] == '{':
                    brace_count += 1
                elif cleaned[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        cleaned = cleaned[start:i+1]
                        break
        else:
            # Found [ first
            start = start_bracket
            # Find matching closing ]
            bracket_count = 0
            for i in range(start, len(cleaned)):
                if cleaned[i] == '[':
                    bracket_count += 1
                elif cleaned[i] == ']':
                    bracket_count -= 1
                    if bracket_count == 0:
                        cleaned = cleaned[start:i+1]
                        break
    
    return cleaned.strip()
