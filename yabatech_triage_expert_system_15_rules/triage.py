"""Educational expert-system demonstration. Not clinical guidance.
All rules and certainty factors are placeholders requiring clinical validation.
"""
URGENCY_RANK={"LOW":1,"MEDIUM":2,"HIGH":3,"EMERGENCY":4}
RULES=[
{"id":"R01","goal":"emergency","conditions":["emergency_signs"],"urgency":"EMERGENCY","referral":"YES","advice":"Follow approved emergency procedures and obtain immediate qualified medical assessment.","certainty_factor":1.0,"explanation":"Emergency-warning option selected."},
{"id":"R02","goal":"high","conditions":["temperature_over_39","persistent_headache"],"urgency":"HIGH","referral":"YES","advice":"Arrange urgent assessment by a qualified clinician.","certainty_factor":0.90,"explanation":"Temperature above 39°C and persistent headache reported."},
{"id":"R03","goal":"high","conditions":["difficulty_breathing"],"urgency":"HIGH","referral":"YES","advice":"Seek immediate qualified clinical assessment; follow local emergency procedures if severe.","certainty_factor":0.95,"explanation":"Difficulty breathing reported."},
{"id":"R04","goal":"high","conditions":["chest_pain"],"urgency":"HIGH","referral":"YES","advice":"Arrange urgent qualified clinical assessment.","certainty_factor":0.95,"explanation":"Chest pain reported."},
{"id":"R05","goal":"high","conditions":["fainting_or_confusion"],"urgency":"HIGH","referral":"YES","advice":"Arrange immediate qualified clinical assessment.","certainty_factor":0.95,"explanation":"Fainting or confusion reported."},
{"id":"R06","goal":"high","conditions":["persistent_vomiting"],"urgency":"HIGH","referral":"REVIEW","advice":"Arrange prompt assessment by a qualified clinician.","certainty_factor":0.80,"explanation":"Persistent vomiting reported."},
{"id":"R07","goal":"high","conditions":["severe_pain"],"urgency":"HIGH","referral":"REVIEW","advice":"Arrange prompt assessment by a qualified clinician.","certainty_factor":0.80,"explanation":"Severe pain reported."},
{"id":"R08","goal":"high","conditions":["temperature_over_39"],"urgency":"HIGH","referral":"REVIEW","advice":"Arrange prompt assessment by a qualified clinician.","certainty_factor":0.75,"explanation":"Temperature above 39°C reported."},
{"id":"R09","goal":"medium","conditions":["fever"],"urgency":"MEDIUM","referral":"REVIEW","advice":"Have a nurse or qualified clinician assess the symptoms.","certainty_factor":0.65,"explanation":"Fever reported without a higher-priority match."},
{"id":"R10","goal":"medium","conditions":["moderate_pain"],"urgency":"MEDIUM","referral":"REVIEW","advice":"Have a nurse or qualified clinician assess the pain.","certainty_factor":0.65,"explanation":"Moderate pain reported."},
{"id":"R11","goal":"medium","conditions":["symptoms_worsening"],"urgency":"MEDIUM","referral":"REVIEW","advice":"Arrange clinical review, particularly if symptoms continue to worsen.","certainty_factor":0.70,"explanation":"Symptoms getting worse reported."},
{"id":"R12","goal":"medium","conditions":["symptoms_persisting"],"urgency":"MEDIUM","referral":"REVIEW","advice":"Arrange clinical review because symptoms are persisting.","certainty_factor":0.65,"explanation":"Persistent symptoms reported."},
{"id":"R13","goal":"low","conditions":["mild_cold","no_fever","no_warning_signs"],"urgency":"LOW","referral":"NO_AUTOMATIC_REFERRAL","advice":"Nurse assessment and appropriate self-care advice; seek review if symptoms worsen.","certainty_factor":0.85,"explanation":"Mild cold without fever or selected warning signs reported."},
{"id":"R14","goal":"low","conditions":["mild_headache","no_fever","no_warning_signs"],"urgency":"LOW","referral":"NO_AUTOMATIC_REFERRAL","advice":"Nurse assessment and appropriate next-step advice; seek review if symptoms worsen.","certainty_factor":0.75,"explanation":"Mild headache without fever or selected warning signs reported."},
{"id":"R15","goal":"review","conditions":["insufficient_information"],"urgency":"MEDIUM","referral":"REVIEW","advice":"No specific rule matched. Refer to a nurse or qualified clinician for assessment.","certainty_factor":0.50,"explanation":"Fallback to human review because the defined rules did not establish a more specific result."},
]
def _facts(d):
    warning=any(bool(d.get(k)) for k in ["emergency_signs","difficulty_breathing","chest_pain","fainting_or_confusion","severe_pain"])
    return {"emergency_signs":bool(d.get("emergency_signs")),
    "temperature_over_39":float(d.get("temperature",0) or 0)>39,
    "persistent_headache":bool(d.get("persistent_headache")),
    "difficulty_breathing":bool(d.get("difficulty_breathing")),"chest_pain":bool(d.get("chest_pain")),
    "fainting_or_confusion":bool(d.get("fainting_or_confusion")),"persistent_vomiting":bool(d.get("persistent_vomiting")),
    "severe_pain":bool(d.get("severe_pain")),"fever":bool(d.get("fever")),"moderate_pain":bool(d.get("moderate_pain")),
    "symptoms_worsening":bool(d.get("symptoms_worsening")),"symptoms_persisting":bool(d.get("symptoms_persisting")),
    "mild_cold":bool(d.get("mild_cold")),"mild_headache":bool(d.get("mild_headache")),
    "no_fever":not bool(d.get("fever")),"no_warning_signs":not warning,"insufficient_information":True}
def backward_chain(goal,facts):
    return [r for r in RULES if r["goal"]==goal and all(facts.get(c,False) for c in r["conditions"])]
def assess_student(data):
    facts=_facts(data); matches=[]
    for goal in ["emergency","high","medium","low","review"]:
        matches.extend(backward_chain(goal,facts))
    if not matches: matches=[RULES[-1]]
    selected=max(matches,key=lambda r:(URGENCY_RANK[r["urgency"]],r["certainty_factor"]))
    result=dict(selected); result["matched_rules"]=[r["id"] for r in matches]
    result["certainty_note"]="Illustrative rule strength only; not a calibrated probability, diagnosis, or assurance of safety."
    return result
