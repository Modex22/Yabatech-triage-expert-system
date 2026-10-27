import unittest
from triage import RULES, assess_student, backward_chain, _facts
def sample(**overrides):
 d={"temperature":37,"persistent_headache":False,"mild_cold":False,"fever":False,"emergency_signs":False,"difficulty_breathing":False,"chest_pain":False,"fainting_or_confusion":False,"persistent_vomiting":False,"severe_pain":False,"moderate_pain":False,"symptoms_worsening":False,"symptoms_persisting":False,"mild_headache":False}; d.update(overrides); return d
class Tests(unittest.TestCase):
 def test_15_rules(self): self.assertEqual(len(RULES),15)
 def test_emergency_priority(self): self.assertEqual(assess_student(sample(emergency_signs=True))["urgency"],"EMERGENCY")
 def test_fever_headache(self): self.assertEqual(assess_student(sample(temperature=39.5,persistent_headache=True,fever=True))["id"],"R02")
 def test_breathing(self): self.assertEqual(assess_student(sample(difficulty_breathing=True))["id"],"R03")
 def test_mild_cold(self): self.assertEqual(assess_student(sample(mild_cold=True))["id"],"R13")
 def test_fallback(self): self.assertEqual(assess_student(sample())["id"],"R15")
 def test_backward_chain(self): self.assertEqual([r["id"] for r in backward_chain("high",_facts(sample(temperature=40,persistent_headache=True)))],["R02","R08"])
if __name__=="__main__": unittest.main()
