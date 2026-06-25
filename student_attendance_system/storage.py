import json, csv, os

DATA_DIR = "data"
STUDENTS_FILE = os.path.join(DATA_DIR, "students.json")
ATTENDANCE_FILE = os.path.join(DATA_DIR, "attendance.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def load_students():
    if not os.path.exists(STUDENTS_FILE):
        return {}
    with open(STUDENTS_FILE) as f:
        return json.load(f)


def save_students(data):
    with open(STUDENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_attendance():
    if not os.path.exists(ATTENDANCE_FILE):
        return []
    with open(ATTENDANCE_FILE, newline="") as f:
        return list(csv.DictReader(f))


def save_attendance(records):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "date", "status"])
        writer.writeheader()
        writer.writerows(records)
