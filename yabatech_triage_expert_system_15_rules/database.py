import sqlite3
from datetime import datetime, timezone
def init_db(path):
    with sqlite3.connect(path) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, temperature REAL NOT NULL,
        urgency TEXT NOT NULL, referral TEXT NOT NULL, rule_id TEXT NOT NULL,
        certainty_factor REAL NOT NULL, explanation TEXT NOT NULL)""")
def save_assessment(path,data,result):
    with sqlite3.connect(path) as c:
        cur=c.execute("INSERT INTO assessments(created_at,temperature,urgency,referral,rule_id,certainty_factor,explanation) VALUES(?,?,?,?,?,?,?)",
        (datetime.now(timezone.utc).isoformat(timespec="seconds"),data["temperature"],result["urgency"],result["referral"],result["id"],result["certainty_factor"],result["explanation"]))
        return cur.lastrowid
def get_recent_assessments(path,limit=50):
    with sqlite3.connect(path) as c:
        c.row_factory=sqlite3.Row
        return [dict(r) for r in c.execute("SELECT * FROM assessments ORDER BY id DESC LIMIT ?",(limit,)).fetchall()]
