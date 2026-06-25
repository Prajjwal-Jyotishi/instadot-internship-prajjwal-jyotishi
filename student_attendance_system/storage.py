"""
storage.py — Persistent file I/O layer (JSON + CSV).
All read/write operations go through this module.
"""

import json
import csv
import os

DATA_DIR      = os.path.join(os.path.dirname(__file__), "data")
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")

ATTENDANCE_FIELDS = ["student_id", "date", "status"]


def _ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


# ── Students (JSON) ──────────────────────────────────────────────────────────

def load_students() -> dict:
    """Return {student_id: {name, course}} dict."""
    _ensure_data_dir()
    if not os.path.exists(STUDENTS_FILE):
        return {}
    with open(STUDENTS_FILE, "r") as f:
        return json.load(f)


def save_students(data: dict) -> None:
    _ensure_data_dir()
    with open(STUDENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── Attendance (CSV) ──────────────────────────────────────────────────────────

def load_attendance() -> list[dict]:
    """Return list of {student_id, date, status} dicts."""
    _ensure_data_dir()
    if not os.path.exists(ATTENDANCE_FILE):
        return []
    with open(ATTENDANCE_FILE, "r", newline="") as f:
        return list(csv.DictReader(f))


def save_attendance(records: list[dict]) -> None:
    _ensure_data_dir()
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=ATTENDANCE_FIELDS)
        writer.writeheader()
        writer.writerows(records)
