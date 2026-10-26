"""Educational, rule-based triage demonstration.

All rules and certainty factors are placeholders. They are not clinical guidance
and must be reviewed and approved by qualified health professionals before use.
"""
URGENCY_RANK = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "EMERGENCY": 4}

RULES = [
    {
        "id": "R0",
        "goal": "emergency_or_immediate_assessment",
        "conditions": ["emergency_signs"],
        "urgency": "EMERGENCY",
        "referral": "YES",
        "advice": "Seek immediate emergency medical assessment and follow local emergency procedures.",
        "certainty_factor": 1.0,
        "explanation": "The emergency-warning input was selected."
    },
    {
        "id": "R1",
        "goal": "high_urgency",
        "conditions": ["temperature_over_39", "persistent_headache"],
        "urgency": "HIGH",
        "referral": "YES",
        "advice": "Arrange urgent assessment by a qualified clinician.",
        "certainty_factor": 0.90,
        "explanation": "Temperature above 39°C and persistent headache were both reported."
    },
    {
        "id": "R2",
        "goal": "low_urgency",
        "conditions": ["mild_cold", "no_fever"],
        "urgency": "LOW",
        "referral": "NO_AUTOMATIC_REFERRAL",
        "advice": "A nurse should assess the student and advise on appropriate self-care.",
        "certainty_factor": 0.85,
        "explanation": "Mild cold symptoms and no fever were reported."
    },
]

def _facts(data):
    """Convert submitted observations into named facts used by the rule engine."""
    return {
        "emergency_signs": bool(data.get("emergency_signs")),
        "temperature_over_39": float(data.get("temperature", 0)) > 39,
        "persistent_headache": bool(data.get("persistent_headache")),
        "mild_cold": bool(data.get("mild_cold")),
        "no_fever": not bool(data.get("fever")),
    }

def backward_chain(goal, facts):
    """Goal-driven backward chaining: try rules that can establish `goal`."""
    matching = []
    for rule in RULES:
        if rule["goal"] != goal:
            continue
        if all(facts.get(condition, False) for condition in rule["conditions"]):
            matching.append(rule)
    return matching

def assess_student(data):
    """Evaluate goals, rank applicable results, and return an explainable result."""
    facts = _facts(data)
    # Query urgent goals first, then lower urgency. This is a simple teaching
    # implementation of goal-directed reasoning and priority ranking.
    goals = [
        "emergency_or_immediate_assessment",
        "high_urgency",
        "low_urgency",
    ]
    candidates = []
    for goal in goals:
        candidates.extend(backward_chain(goal, facts))

    if candidates:
        selected = max(
            candidates,
            key=lambda rule: (
                URGENCY_RANK[rule["urgency"]],
                rule["certainty_factor"]
            )
        )
        result = dict(selected)
        result["matched_rules"] = [r["id"] for r in candidates]
        result["certainty_note"] = (
            "Illustrative rule strength only; not a calibrated probability or diagnosis."
        )
        return result

    return {
        "id": "R3",
        "goal": "needs_clinician_review",
        "urgency": "MEDIUM",
        "referral": "REVIEW",
        "advice": "A nurse or qualified clinician must assess the student and decide the next step.",
        "certainty_factor": 0.50,
        "explanation": "No defined rule matched all required conditions.",
        "matched_rules": [],
        "certainty_note": "Fallback value is illustrative only; uncertainty requires human review."
    }
