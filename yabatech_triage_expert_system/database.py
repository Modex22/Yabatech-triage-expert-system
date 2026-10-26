import json
import sqlite3
from datetime import datetime, timezone

def init_db(path):
    with sqlite3.connect(path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                temperature REAL NOT NULL,
                persistent_headache INTEGER NOT NULL,
                mild_cold INTEGER NOT NULL,
                fever INTEGER NOT NULL,
                emergency_signs INTEGER NOT NULL,
                urgency TEXT NOT NULL,
                referral TEXT NOT NULL,
                rule_id TEXT NOT NULL,
                certainty_factor REAL NOT NULL,
                explanation TEXT NOT NULL
            )
        """)
        conn.commit()

def save_assessment(path, data, result):
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    with sqlite3.connect(path) as conn:
        cur = conn.execute("""
            INSERT INTO assessments
            (created_at, temperature, persistent_headache, mild_cold, fever,
             emergency_signs, urgency, referral, rule_id, certainty_factor, explanation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            created_at, data["temperature"], int(data["persistent_headache"]),
            int(data["mild_cold"]), int(data["fever"]), int(data["emergency_signs"]),
            result["urgency"], result["referral"], result["id"],
            result["certainty_factor"], result["explanation"]
        ))
        conn.commit()
        return cur.lastrowid

def get_recent_assessments(path, limit=50):
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT id, created_at, temperature, urgency, referral, rule_id,
                   certainty_factor, explanation
            FROM assessments ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()
        return [dict(row) for row in rows]
