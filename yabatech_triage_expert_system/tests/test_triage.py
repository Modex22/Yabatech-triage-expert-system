import unittest
from triage import assess_student, backward_chain, _facts

class TriageTests(unittest.TestCase):
    def test_emergency_has_highest_priority(self):
        result = assess_student({
            "temperature": 40, "persistent_headache": True,
            "mild_cold": True, "fever": True, "emergency_signs": True
        })
        self.assertEqual(result["urgency"], "EMERGENCY")
        self.assertEqual(result["id"], "R0")

    def test_high_temperature_and_headache(self):
        result = assess_student({
            "temperature": 39.5, "persistent_headache": True,
            "mild_cold": False, "fever": True, "emergency_signs": False
        })
        self.assertEqual(result["urgency"], "HIGH")
        self.assertEqual(result["referral"], "YES")
        self.assertEqual(result["id"], "R1")

    def test_mild_cold_without_fever(self):
        result = assess_student({
            "temperature": 36.8, "persistent_headache": False,
            "mild_cold": True, "fever": False, "emergency_signs": False
        })
        self.assertEqual(result["urgency"], "LOW")
        self.assertEqual(result["id"], "R2")

    def test_no_rule_falls_back_to_human_review(self):
        result = assess_student({
            "temperature": 37, "persistent_headache": False,
            "mild_cold": False, "fever": False, "emergency_signs": False
        })
        self.assertEqual(result["urgency"], "MEDIUM")
        self.assertEqual(result["referral"], "REVIEW")

    def test_backward_chaining_checks_goal(self):
        facts = _facts({
            "temperature": 40, "persistent_headache": True,
            "mild_cold": False, "fever": True, "emergency_signs": False
        })
        self.assertEqual([r["id"] for r in backward_chain("high_urgency", facts)], ["R1"])
        self.assertEqual(backward_chain("low_urgency", facts), [])

if __name__ == "__main__":
    unittest.main()
