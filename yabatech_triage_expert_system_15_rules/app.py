import os
from flask import Flask, render_template, request, redirect, url_for, flash
from triage import assess_student
from database import init_db, save_assessment, get_recent_assessments

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-only-change-me")
os.makedirs("instance", exist_ok=True)
DB = os.environ.get("TRIAGE_DATABASE", "instance/triage.sqlite3")
init_db(DB)

FIELDS = ["persistent_headache","mild_cold","fever","emergency_signs",
"difficulty_breathing","chest_pain","fainting_or_confusion","persistent_vomiting",
"severe_pain","moderate_pain","symptoms_worsening","symptoms_persisting","mild_headache"]

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        try:
            temp=float(request.form.get("temperature",""))
            if not 30 <= temp <= 45: raise ValueError()
        except ValueError:
            flash("Enter a temperature between 30°C and 45°C.","error")
            return redirect(url_for("index"))
        data={"temperature":temp}
        data.update({f: request.form.get(f)=="yes" for f in FIELDS})
        result=assess_student(data)
        record_id=save_assessment(DB,data,result)
        return render_template("result.html",result=result,record_id=record_id)
    return render_template("index.html")

@app.route("/history")
def history():
    return render_template("history.html",records=get_recent_assessments(DB))

@app.route("/health")
def health():
    return {"status":"ok"}

if __name__=="__main__":
    app.run(debug=False)
