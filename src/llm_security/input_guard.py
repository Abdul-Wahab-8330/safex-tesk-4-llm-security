import re


ATTACK_PATTERNS = {
    "instruction_override": [
        (
            r"\b(ignore|disregard)\b.{0,80}"
            r"\b(all|your|previous|prior|above|system|application|provided)\b"
            r".{0,40}\b(instructions|rules|policies|restrictions)\b"
        ),
        (
            r"\b(ignore|disregard)\b.{0,80}"
            r"\b(rules|instructions|policies)\b.{0,50}"
            r"\b(application|system|security|safety)\b"
        ),
        r"\b(follow only my instructions|follow my instructions instead)\b",
        (
            r"\b(override|bypass|disable|remove)\b.{0,80}"
            r"\b(system|application|security|safety)\s+"
            r"(instructions|rules|policies|restrictions)\b"
        ),
        (
            r"\bforget\b.{0,60}"
            r"\b(system instructions|system prompt|system message|"
            r"hidden instructions|security rules)\b"
        ),
    ],

    "role_manipulation": [
        r"\byou are no longer\b",
        r"\bunrestricted (ai|assistant|model)\b",
        r"\bact as (an? )?(unrestricted|unfiltered)\b",
        r"\bpretend\b.{0,100}\b(restrictions|rules)\b",
    ],

    "system_prompt_extraction": [
        (
            r"\b(reveal|print|show|reproduce|summarize|tell me)\b"
            r".{0,100}\b(system prompt|system message|"
            r"system instructions|hidden instructions)\b"
        ),
        r"\bexact system (message|prompt|instructions)\b",
    ],
}


def validate_input(user_input):
    """
    Heuristically classify user input against known attack patterns.

    This is a lightweight filter, not a complete prompt-injection detector.
    """
    if not isinstance(user_input, str) or not user_input.strip():
        return {
            "allowed": False,
            "reason": "empty_or_invalid_input",
        }

    for category, patterns in ATTACK_PATTERNS.items():
        for pattern in patterns:
            if re.search(
                pattern,
                user_input,
                flags=re.IGNORECASE | re.DOTALL,
            ):
                return {
                    "allowed": False,
                    "reason": category,
                }

    return {
        "allowed": True,
        "reason": "no_known_pattern_detected",
    }