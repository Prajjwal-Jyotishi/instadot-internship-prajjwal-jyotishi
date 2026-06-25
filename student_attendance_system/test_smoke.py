import sys, os, shutil
sys.path.insert(0, os.path.dirname(__file__))

import storage
storage.DATA_DIR = os.path.join(os.path.dirname(__file__), "data_test")
storage.STUDENTS_FILE = os.path.join(storage.DATA_DIR, "students.json")
storage.ATTENDANCE_FILE = os.path.join(storage.DATA_DIR, "attendance.csv")
os.makedirs(storage.DATA_DIR, exist_ok=True)

from system import (register_student, search_student, list_students, delete_student,
                    mark_attendance, update_attendance, attendance_percentage, monthly_report)

print("=== Smoke Test ===\n")

register_student("S001", "Prajjwal", "Python")
register_student("S002", "Anjali", "Data Science")
register_student("S001", "Dup", "Test")

print()
search_student("S001")
search_student("S999")

list_students()

print()
for d, s in [("2026-06-01","P"),("2026-06-02","A"),("2026-06-03","P"),("2026-06-04","L"),("2026-06-05","P")]:
    mark_attendance("S001", d, s)
for d, s in [("2026-06-01","P"),("2026-06-02","P"),("2026-06-03","A")]:
    mark_attendance("S002", d, s)
mark_attendance("S001", "2026-06-01", "P")  # duplicate

print()
update_attendance("S001", "2026-06-02", "L")
update_attendance("S001", "2099-01-01", "P")

print()
attendance_percentage("S001")
attendance_percentage("S002")
attendance_percentage("S999")

monthly_report(2026, 6)

delete_student("S002")
delete_student("S999")

shutil.rmtree(storage.DATA_DIR, ignore_errors=True)
print("All tests done.")
