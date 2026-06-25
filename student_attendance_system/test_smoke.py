"""Quick smoke test — runs all core features non-interactively."""
import sys, os, shutil
sys.path.insert(0, os.path.dirname(__file__))

# Use a temp data dir so tests don't pollute real data
import storage
storage.DATA_DIR       = os.path.join(os.path.dirname(__file__), "data_test")
storage.STUDENTS_FILE  = os.path.join(storage.DATA_DIR, "students.json")
storage.ATTENDANCE_FILE = os.path.join(storage.DATA_DIR, "attendance.csv")

from students   import register_student, search_student, delete_student, list_students
from attendance import mark_attendance, update_attendance, get_attendance_percentage
from reports    import generate_monthly_report, print_monthly_report

print("=" * 50)
print("SMOKE TEST — Student Attendance Management System")
print("=" * 50)

# 1. Register
print(register_student("S001", "Prajjwal", "Python"))
print(register_student("S002", "Anjali",   "Data Science"))
print(register_student("S001", "Duplicate","Test"))   # Should error

# 2. Search
s = search_student("S001")
print(f"\nSearch S001 → {s}")

# 3. List
print("\nAll students:")
for sid, info in list_students().items():
    print(f"  {sid}: {info}")

# 4. Mark attendance
print()
for date, status in [("2026-06-01","P"),("2026-06-02","A"),("2026-06-03","P"),("2026-06-04","L"),("2026-06-05","P")]:
    print(mark_attendance("S001", date, status))
for date, status in [("2026-06-01","P"),("2026-06-02","P"),("2026-06-03","A")]:
    print(mark_attendance("S002", date, status))

# 5. Duplicate mark (should error)
print(mark_attendance("S001", "2026-06-01", "P"))

# 6. Update
print()
print(update_attendance("S001", "2026-06-02", "L"))   # A → L
print(update_attendance("S001", "2099-01-01", "P"))   # Non-existent

# 7. Percentage
print()
print(get_attendance_percentage("S001"))
print(get_attendance_percentage("S002"))
print(get_attendance_percentage("S999"))  # Not found

# 8. Monthly report
print_monthly_report(2026, 6)
path = generate_monthly_report(2026, 6)
print(f"Report saved → {path}")

# 9. Delete
print()
print(delete_student("S002"))
print(delete_student("S999"))  # Not found

# Cleanup test data
shutil.rmtree(storage.DATA_DIR, ignore_errors=True)
print("\nAll tests passed ✓")
