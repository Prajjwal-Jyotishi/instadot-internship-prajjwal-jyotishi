"""
attendance.py — Mark, Update, Percentage Calculation, Monthly summary.
"""

from datetime import date as date_type
from storage import load_attendance, save_attendance
from students import search_student


def _validate_status(status: str) -> bool:
    return status.upper() in ("P", "A", "L")   # Present / Absent / Leave


def mark_attendance(student_id: str, date: str, status: str) -> str:
    """Mark attendance for a student on a given date (YYYY-MM-DD)."""
    if not search_student(student_id):
        return f"[ERROR] Student ID '{student_id}' not found."
    status = status.upper()
    if not _validate_status(status):
        return "[ERROR] Status must be P (Present), A (Absent), or L (Leave)."

    records = load_attendance()
    for r in records:
        if r["student_id"] == student_id and r["date"] == date:
            return f"[ERROR] Attendance for '{student_id}' on {date} already marked. Use update instead."

    records.append({"student_id": student_id, "date": date, "status": status})
    save_attendance(records)
    return f"[OK] Attendance marked — {student_id} | {date} | {status}."


def update_attendance(student_id: str, date: str, new_status: str) -> str:
    """Update an existing attendance entry."""
    new_status = new_status.upper()
    if not _validate_status(new_status):
        return "[ERROR] Status must be P (Present), A (Absent), or L (Leave)."

    records = load_attendance()
    for r in records:
        if r["student_id"] == student_id and r["date"] == date:
            old = r["status"]
            r["status"] = new_status
            save_attendance(records)
            return f"[OK] Updated {student_id} | {date}: {old} → {new_status}."

    return f"[ERROR] No attendance record found for '{student_id}' on {date}."


def get_attendance_percentage(student_id: str) -> str:
    """Calculate overall attendance percentage for a student."""
    if not search_student(student_id):
        return f"[ERROR] Student ID '{student_id}' not found."

    records = [r for r in load_attendance() if r["student_id"] == student_id]
    if not records:
        return f"[INFO] No attendance records found for '{student_id}'."

    total   = len(records)
    present = sum(1 for r in records if r["status"] == "P")
    pct     = (present / total) * 100
    return f"[RESULT] {student_id} — {present}/{total} days present | {pct:.1f}% attendance."


def get_monthly_summary(student_id: str, year: int, month: int) -> list[dict]:
    """Return attendance records for a student filtered by year & month."""
    prefix = f"{year}-{month:02d}"
    return [
        r for r in load_attendance()
        if r["student_id"] == student_id and r["date"].startswith(prefix)
    ]
