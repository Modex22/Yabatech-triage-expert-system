import os
from flask import Flask, render_template, request, redirect, url_for, flash
from triage import assess_student
from database import init_db, save_assessment, get_recent_assessments

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
DATABASE = os.environ.get("TRIAGE_DATABASE", os.path.join(app.instance_path, "triage.sqlite3"))
os.makedirs(app.instance_path, exist_ok=True)
init_db(DATABASE)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            temperature = float(request.form.get("temperature", ""))
            if not 30 <= temperature <= 45:
                raise ValueError("Temperature must be between 30°C and 45°C.")
        except ValueError:
            flash("Enter a valid temperature between 30°C and 45°C.", "error")
            return redirect(url_for("index"))

        data = {
            "temperature": temperature,
            "persistent_headache": request.form.get("persistent_headache") == "yes",
            "mild_cold": request.form.get("mild_cold") == "yes",
            "fever": request.form.get("fever") == "yes",
            "emergency_signs": request.form.get("emergency_signs") == "yes",
        }
        result = assess_student(data)
        # Do not collect names or matriculation numbers in this teaching prototype.
        record_id = save_assessment(DATABASE, data, result)
        return render_template("result.html", result=result, record_id=record_id)

    return render_template("index.html")

@app.route("/history")
def history():
    records = get_recent_assessments(DATABASE)
    return render_template("history.html", records=records)

@app.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    # Development server only. Use a production WSGI server for deployment.
    app.run(debug=False)
