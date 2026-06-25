import csv, os, threading
from datetime import datetime
from storage import load_students, save_students, load_attendance, save_attendance, DATA_DIR


# ---- Student Operations ----

def register_student(sid, name, course):
    students = load_students()
    if sid in students:
        print(f"Student ID '{sid}' already exists.")
        return
    students[sid] = {"name": name, "course": course}
    save_students(students)
    print(f"Student '{name}' registered successfully.")


def search_student(sid):
    students = load_students()
    if sid not in students:
        print(f"Student '{sid}' not found.")
        return
    info = students[sid]
    print(f"\nID: {sid}  |  Name: {info['name']}  |  Course: {info['course']}")


def list_students():
    students = load_students()
    if not students:
        print("No students registered yet.")
        return
    print(f"\n{'ID':<12} {'Name':<20} {'Course'}")
    print("-" * 45)
    for sid, info in students.items():
        print(f"{sid:<12} {info['name']:<20} {info['course']}")


def delete_student(sid):
    students = load_students()
    if sid not in students:
        print(f"Student '{sid}' not found.")
        return
    print(f"Student '{students.pop(sid)['name']}' deleted.")
    save_students(students)


# ---- Attendance Operations ----

def mark_attendance(sid, att_date, status):
    if sid not in load_students():
        print(f"Student '{sid}' not found.")
        return
    status = status.upper()
    if status not in ("P", "A", "L"):
        print("Invalid status. Use P, A, or L.")
        return
    records = load_attendance()
    if any(r["student_id"] == sid and r["date"] == att_date for r in records):
        print(f"Attendance for '{sid}' on {att_date} already marked.")
        return
    records.append({"student_id": sid, "date": att_date, "status": status})
    save_attendance(records)
    print(f"Marked: {sid} | {att_date} | {status}")


def update_attendance(sid, att_date, new_status):
    new_status = new_status.upper()
    if new_status not in ("P", "A", "L"):
        print("Invalid status. Use P, A, or L.")
        return
    records = load_attendance()
    for r in records:
        if r["student_id"] == sid and r["date"] == att_date:
            r["status"] = new_status
            save_attendance(records)
            print(f"Updated: {sid} | {att_date} -> {new_status}")
            return
    print(f"No record found for '{sid}' on {att_date}.")


def attendance_percentage(sid):
    students = load_students()
    if sid not in students:
        print(f"Student '{sid}' not found.")
        return
    records = [r for r in load_attendance() if r["student_id"] == sid]
    if not records:
        print(f"No attendance records for '{sid}'.")
        return
    present = sum(1 for r in records if r["status"] == "P")
    print(f"\n{students[sid]['name']} ({sid}): {present}/{len(records)} days | {present/len(records)*100:.1f}%")


# ---- Reports ----

def monthly_report(year, month):
    students = load_students()
    records = load_attendance()
    prefix = f"{year}-{month:02d}"

    print(f"\n{'='*50}")
    print(f"  Monthly Report - {month:02d}/{year}")
    print(f"{'='*50}")
    print(f"{'ID':<10} {'Name':<20} {'P':>4} {'A':>4} {'L':>4} {'%':>6}")
    print(f"{'-'*50}")

    report_rows = []
    for sid, info in students.items():
        recs = [r for r in records if r["student_id"] == sid and r["date"].startswith(prefix)]
        total = len(recs)
        p = sum(1 for r in recs if r["status"] == "P")
        a = sum(1 for r in recs if r["status"] == "A")
        l = sum(1 for r in recs if r["status"] == "L")
        pct = round(p / total * 100, 1) if total else 0.0
        print(f"{sid:<10} {info['name']:<20} {p:>4} {a:>4} {l:>4} {pct:>5.1f}%")
        report_rows.append({"student_id": sid, "name": info["name"], "present": p, "absent": a, "leave": l, "percentage": pct})

    print(f"{'='*50}")

    path = os.path.join(DATA_DIR, f"report_{year}_{month:02d}.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "name", "present", "absent", "leave", "percentage"])
        writer.writeheader()
        writer.writerows(report_rows)
    print(f"Report saved: {path}\n")


def auto_report():
    now = datetime.now()
    print(f"\n[Background] Auto-generating report for {now.month:02d}/{now.year}...")
    monthly_report(now.year, now.month)


def run_report_in_background():
    t = threading.Thread(target=auto_report, daemon=True)
    t.start()
    return t
