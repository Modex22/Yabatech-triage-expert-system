# YABATECH Student Health Centre Triage Expert System — Project Report

## 1. Introduction
This project demonstrates a rule-based expert system that organizes symptom observations and suggests an urgency category for coursework. It is not a diagnostic tool and is not approved for real clinical use.

## 2. Background and Problem Statement
The case scenario describes concerns about limited bed space and inconsistent diagnosis quality at the YABATECH Health Centre. A consistent decision-support prototype can demonstrate how rules and explanations might support nurse workflow while leaving real decisions to qualified professionals.

## 3. Aim and Objectives
**Aim:** Design a rule-based triage expert-system prototype. Objectives: collect symptom inputs, apply production rules, demonstrate backward chaining and priority ranking, show illustrative certainty factors, store test assessments, and test expected rule behavior.

## 4. System Requirements
Functional: symptom form, rule evaluation, urgency/referral output, explanation, certainty display, SQLite history. Non-functional: simple interface, modular code, validation, transparency. Real use would require clinical governance and security controls.

## 5. Knowledge Acquisition
The case brief supplied the starting scenario. The expanded rules here are illustrative coursework examples, not sourced from an approved clinical protocol. A real project would require interviews with qualified clinicians and review of approved local guidance.

## 6. Knowledge Representation
Production rules use IF conditions THEN conclusion/action. Each rule stores an ID, goal, conditions, urgency, referral recommendation, explanation and illustrative certainty factor.

## 7. Fifteen IF–THEN Rules
All rules below are placeholders and require clinical validation.
| ID | IF | THEN |
|---|---|---|
| R01 | Emergency-warning option selected | EMERGENCY; follow approved emergency procedure |
| R02 | Temperature >39°C AND persistent headache | HIGH; urgent clinician assessment |
| R03 | Difficulty breathing reported | HIGH; immediate qualified assessment |
| R04 | Chest pain reported | HIGH; urgent qualified assessment |
| R05 | Fainting or confusion reported | HIGH; immediate qualified assessment |
| R06 | Persistent vomiting reported | HIGH; prompt clinical assessment |
| R07 | Severe pain reported | HIGH; prompt clinical assessment |
| R08 | Temperature >39°C | HIGH; prompt clinical assessment |
| R09 | Fever reported and no higher rule matches | MEDIUM; nurse/clinician review |
| R10 | Moderate pain reported and no higher rule matches | MEDIUM; clinician review |
| R11 | Symptoms worsening and no higher rule matches | MEDIUM; clinical review |
| R12 | Symptoms persisting and no higher rule matches | MEDIUM; clinical review |
| R13 | Mild cold AND no fever AND no selected warning signs | LOW; nurse assessment and appropriate advice |
| R14 | Mild headache AND no fever AND no selected warning signs | LOW; nurse assessment and appropriate advice |
| R15 | No more specific rule applies | MEDIUM/REVIEW; human assessment |

## 8. Inference Strategy: Backward Chaining
The engine starts with goals such as emergency, high, medium or low urgency and checks whether facts satisfy the conditions of rules that establish those goals. It tests higher-priority goals before lower-priority ones. This is appropriate for a goal-oriented urgency question.

## 9. Certainty Factors
Each rule has a value from 0 to 1 to demonstrate uncertainty representation. These are not calibrated probabilities, clinical confidence estimates or assurances of safety. Uncertainty should lead to qualified human review.

## 10. Priority Ranking
Priority is EMERGENCY > HIGH > MEDIUM > LOW. The highest urgency wins when several rules match; certainty only breaks ties at the same urgency. This illustrative hierarchy needs clinical approval before real use.

## 11. Architecture
Presentation layer: Flask templates. Knowledge base and inference engine: `triage.py`. Database layer: `database.py` with SQLite. Outputs include urgency, referral recommendation, matched rules, explanation and illustrative certainty factor.

## 12. Development Tools
Python implements logic; Flask handles routes; HTML/CSS provides the interface; SQLite stores local demo records; `unittest` checks behavior; Railway may host a non-clinical demonstration.

## 13. Testing and Results
Automated tests check the 15-rule count, emergency priority, high-temperature/headache match, breathing-difficulty priority, mild-cold rule, fallback behavior and backward chaining. These tests verify software behavior, not clinical correctness.

## 14. Limitations and Recommendations
Rules are simplified, incomplete and unvalidated. The prototype cannot replace examination, clinical judgement or approved triage protocols. Real use would require clinical validation, access controls, privacy safeguards, audit logs, secure hosting, managed persistence and emergency escalation procedures.

## 15. Conclusion
The prototype demonstrates production rules, backward chaining, illustrative certainty factors, priority ranking, a Flask interface and SQLite storage. Its rules must not be used for diagnosis or treatment without formal clinical approval and validation.
