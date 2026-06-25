"""
main.py — Student Attendance Management System
Entry point with interactive CLI menu.
"""

import sys
import os
from datetime import datetime

# Ensure imports resolve from the same directory
sys.path.insert(0, os.path.dirname(__file__))

from students   import register_student, search_student, list_students, delete_student
from attendance import mark_attendance, update_attendance, get_attendance_percentage
from reports    import print_monthly_report, generate_monthly_report, auto_generate_report


# ── Helpers ───────────────────────────────────────────────────────────────────

def _input(prompt: str) -> str:
    return input(prompt).strip()

def _divider():
    print("-" * 45)

def _header(title: str):
    print(f"\n{'='*45}")
    print(f"  {title}")
    print(f"{'='*45}")


# ── Menu Handlers ─────────────────────────────────────────────────────────────

def handle_register():
    _header("Register Student")
    sid    = _input("Student ID   : ")
    name   = _input("Name         : ")
    course = _input("Course       : ")
    print(register_student(sid, name, course))


def handle_search():
    _header("Search Student")
    sid  = _input("Student ID: ")
    data = search_student(sid)
    if data:
        print(f"\n  ID     : {sid}")
        print(f"  Name   : {data['name']}")
        print(f"  Course : {data['course']}")
    else:
        print(f"[ERROR] Student '{sid}' not found.")


def handle_list():
    _header("All Students")
    students = list_students()
    if not students:
        print("  No students registered yet.")
        return
    print(f"{'ID':<12} {'Name':<20} {'Course'}")
    _divider()
    for sid, info in students.items():
        print(f"{sid:<12} {info['name']:<20} {info['course']}")


def handle_delete():
    _header("Delete Student")
    sid = _input("Student ID: ")
    confirm = _input(f"Delete '{sid}'? (yes/no): ")
    if confirm.lower() == "yes":
        print(delete_student(sid))
    else:
        print("[CANCELLED] No changes made.")


def handle_mark():
    _header("Mark Attendance")
    sid    = _input("Student ID    : ")
    date   = _input("Date (YYYY-MM-DD) [Enter for today]: ") or datetime.now().strftime("%Y-%m-%d")
    status = _input("Status (P/A/L): ")
    print(mark_attendance(sid, date, status))


def handle_update():
    _header("Update Attendance")
    sid    = _input("Student ID        : ")
    date   = _input("Date (YYYY-MM-DD) : ")
    status = _input("New Status (P/A/L): ")
    print(update_attendance(sid, date, status))


def handle_percentage():
    _header("Attendance Percentage")
    sid = _input("Student ID: ")
    print(get_attendance_percentage(sid))


def handle_monthly_report():
    _header("Monthly Report")
    now   = datetime.now()
    year  = _input(f"Year  [{now.year}] : ") or str(now.year)
    month = _input(f"Month [{now.month:02d}]  : ") or str(now.month)
    try:
        print_monthly_report(int(year), int(month))
        path = generate_monthly_report(int(year), int(month))
        print(f"[SAVED] Report exported → {path}")
    except ValueError:
        print("[ERROR] Invalid year/month.")


# ── Main Menu ─────────────────────────────────────────────────────────────────

MENU = """
╔══════════════════════════════════════════╗
║   Student Attendance Management System  ║
╠══════════════════════════════════════════╣
║  1. Register Student                    ║
║  2. Search Student                      ║
║  3. List All Students                   ║
║  4. Delete Student                      ║
║  5. Mark Attendance                     ║
║  6. Update Attendance                   ║
║  7. Attendance Percentage               ║
║  8. Monthly Report                      ║
║  0. Exit                                ║
╚══════════════════════════════════════════╝
"""

ACTIONS = {
    "1": handle_register,
    "2": handle_search,
    "3": handle_list,
    "4": handle_delete,
    "5": handle_mark,
    "6": handle_update,
    "7": handle_percentage,
    "8": handle_monthly_report,
}


def main():
    # Ensure Unicode renders correctly on Windows terminals
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("\nWelcome to Student Attendance Management System")
    while True:
        print(MENU)
        choice = _input("Enter choice: ")
        if choice == "0":
            print("\n[EXIT] Generating auto-report in background...")
            t = auto_generate_report()
            t.join(timeout=5)          # Wait up to 5s for background report
            print("Goodbye!")
            break
        action = ACTIONS.get(choice)
        if action:
            try:
                action()
            except KeyboardInterrupt:
                print("\n[CANCELLED]")
            except Exception as e:
                print(f"[UNEXPECTED ERROR] {e}")
        else:
            print("[ERROR] Invalid choice. Please enter 0–8.")


if __name__ == "__main__":
    main()
