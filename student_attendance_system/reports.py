"""
reports.py — Monthly Attendance Report generation.
Bonus: auto_generate_report() runs in a background thread on program exit.
"""

import csv
import os
import threading
from datetime import datetime

from storage import load_attendance, load_students, DATA_DIR


def generate_monthly_report(year: int, month: int) -> str:
    """
    Generate a CSV report for all students for the given month.
    Saved to data/report_YYYY_MM.csv
    """
    students  = load_students()
    records   = load_attendance()
    prefix    = f"{year}-{month:02d}"

    # Build summary: {student_id: {P, A, L, total, pct}}
    summary = {}
    for sid, info in students.items():
        month_recs = [r for r in records if r["student_id"] == sid and r["date"].startswith(prefix)]
        total   = len(month_recs)
        present = sum(1 for r in month_recs if r["status"] == "P")
        absent  = sum(1 for r in month_recs if r["status"] == "A")
        leave   = sum(1 for r in month_recs if r["status"] == "L")
        pct     = round((present / total * 100), 1) if total else 0.0
        summary[sid] = {
            "student_id":  sid,
            "name":        info["name"],
            "course":      info["course"],
            "total_days":  total,
            "present":     present,
            "absent":      absent,
            "leave":       leave,
            "percentage":  pct,
        }

    report_file = os.path.join(DATA_DIR, f"report_{year}_{month:02d}.csv")
    fields = ["student_id", "name", "course", "total_days", "present", "absent", "leave", "percentage"]

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(report_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(summary.values())

    return report_file


def print_monthly_report(year: int, month: int) -> None:
    """Print a formatted monthly report to the console."""
    students  = load_students()
    records   = load_attendance()
    prefix    = f"{year}-{month:02d}"

    print(f"\n{'='*60}")
    print(f"  Monthly Attendance Report — {month:02d}/{year}")
    print(f"{'='*60}")
    print(f"{'ID':<10} {'Name':<20} {'Course':<15} {'P':>4} {'A':>4} {'L':>4} {'%':>6}")
    print(f"{'-'*60}")

    if not students:
        print("  No students registered.")
    else:
        for sid, info in students.items():
            recs    = [r for r in records if r["student_id"] == sid and r["date"].startswith(prefix)]
            total   = len(recs)
            present = sum(1 for r in recs if r["status"] == "P")
            absent  = sum(1 for r in recs if r["status"] == "A")
            leave   = sum(1 for r in recs if r["status"] == "L")
            pct     = (present / total * 100) if total else 0.0
            print(f"{sid:<10} {info['name']:<20} {info['course']:<15} {present:>4} {absent:>4} {leave:>4} {pct:>5.1f}%")

    print(f"{'='*60}\n")


# ── Bonus: Background Auto-Report ────────────────────────────────────────────

def _background_report_task():
    """Silently generate this month's report in the background."""
    now  = datetime.now()
    path = generate_monthly_report(now.year, now.month)
    print(f"\n[AUTO-REPORT] Monthly report saved → {path}")


def auto_generate_report() -> threading.Thread:
    """
    Spawn a daemon thread that generates the current month's report.
    Call this after the main menu exits.
    """
    t = threading.Thread(target=_background_report_task, daemon=True)
    t.start()
    return t
