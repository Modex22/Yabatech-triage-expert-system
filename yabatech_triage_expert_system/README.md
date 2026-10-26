# YABATECH Student Health Centre Triage Expert System

A Flask + SQLite educational prototype demonstrating a rule-based expert system, goal-driven backward chaining, illustrative certainty factors, priority ranking, and unit tests.

## Important safety limitation

This project is for coursework and demonstration only. It is **not a medical device, diagnostic tool, or approved clinical triage system**. The rules, thresholds, emergency-warning input, advice, and certainty factors are illustrative placeholders. A qualified clinical team must define and approve all rules, validate them, test failure modes, and establish local emergency/referral procedures before any real-world use. Never delay emergency care to complete this form.

Use anonymized test data only. The prototype intentionally does not collect student names or matriculation numbers. The history page is not authentication-protected and should only be used locally with test data.

## Requirements

- Python 3.10 or newer
- pip
- A terminal / command prompt

## Setup

### 1. Extract and enter the project folder

```bash
cd yabatech_triage_expert_system
```

### 2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -m venv .venv
.venv\\Scripts\\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the website

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser. SQLite database is created automatically at `instance/triage.sqlite3`.

### 5. Run the tests

Stop the web server if running, then run:

```bash
python -m unittest discover -s tests -v
```

Five tests cover emergency priority, high urgency, low urgency, fallback to clinician review, and backward chaining.

## How the system works

- **Knowledge base:** `RULES` in `triage.py` stores the demonstration rules.
- **Inference engine:** `assess_student()` builds facts from input, checks target goals, and ranks matched rules.
- **Backward chaining:** `backward_chain(goal, facts)` starts from a target goal and checks whether all conditions for a rule establishing that goal are true.
- **Priority ranking:** emergency > high > medium > low. The fallback medium result is used when no rule matches. The explicit emergency-warning input has highest priority.
- **Certainty factors:** values between 0 and 1 are shown to demonstrate the concept. They are not calibrated probabilities and must not be used to decide care.
- **SQLite:** `database.py` stores limited assessment fields and result summaries.

## Rule summary

| Rule | Conditions | Demonstration result |
|---|---|---|
| R0 | Emergency warning input selected | EMERGENCY; immediate assessment |
| R1 | Temperature > 39°C AND persistent headache | HIGH; urgent clinician assessment |
| R2 | Mild cold AND no fever | LOW; nurse assessment / appropriate self-care advice |
| R3 | No defined rule matches | MEDIUM; clinician review |

These are assignment examples, not medically validated rules.

## Before any deployment

Do not deploy this as a live clinical service. A production system would require clinical governance, approved and validated rules, privacy/security review, authentication and role-based access, audit controls, encrypted transport/storage, backups, monitoring, accessibility testing, and a documented emergency escalation process. Set a strong `FLASK_SECRET_KEY`; use a production WSGI server and appropriate hosting configuration if deploying a non-clinical demonstration.


## Deploy to Render

This repository includes `render.yaml` and `gunicorn` for Render deployment.

1. Push the project folder to a GitHub repository.
2. In Render, choose **New + → Blueprint** and connect that GitHub repository, or create a **New + → Web Service** from the repo.
3. For a Web Service, use:
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Health check path: `/health`
4. Deploy and open the `onrender.com` URL shown by Render.

### SQLite persistence warning

Render's free web services use an ephemeral filesystem. This means assessment records in the local SQLite database can be lost when the service restarts, spins down, or redeploys. This is acceptable only for a demo using non-sensitive test data. To retain SQLite records, use a paid Render web service with a persistent disk mounted at `/var/data`, and set `TRIAGE_DATABASE=/var/data/triage.sqlite3` in the service's environment variables. For a more robust hosted database, consider managed PostgreSQL. Never use this educational prototype for real patient records.
