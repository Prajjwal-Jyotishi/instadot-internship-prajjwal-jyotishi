import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from system import (register_student, search_student, list_students, delete_student,
                    mark_attendance, update_attendance, attendance_percentage,
                    monthly_report, run_report_in_background)


def main():
    while True:
        print("\n--- Student Attendance Management System ---")
        print("1. Register Student")
        print("2. Search Student")
        print("3. List All Students")
        print("4. Delete Student")
        print("5. Mark Attendance")
        print("6. Update Attendance")
        print("7. Attendance Percentage")
        print("8. Monthly Report")
        print("0. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == "1":
            register_student(input("Student ID: ").strip(), input("Name: ").strip(), input("Course: ").strip())

        elif choice == "2":
            search_student(input("Student ID: ").strip())

        elif choice == "3":
            list_students()

        elif choice == "4":
            sid = input("Student ID: ").strip()
            if input(f"Delete '{sid}'? (yes/no): ").strip().lower() == "yes":
                delete_student(sid)
            else:
                print("Cancelled.")

        elif choice == "5":
            sid = input("Student ID: ").strip()
            date = input("Date (YYYY-MM-DD) [blank = today]: ").strip() or datetime.now().strftime("%Y-%m-%d")
            mark_attendance(sid, date, input("Status (P/A/L): ").strip())

        elif choice == "6":
            update_attendance(input("Student ID: ").strip(), input("Date (YYYY-MM-DD): ").strip(), input("New Status (P/A/L): ").strip())

        elif choice == "7":
            attendance_percentage(input("Student ID: ").strip())

        elif choice == "8":
            now = datetime.now()
            year = input(f"Year [{now.year}]: ").strip() or str(now.year)
            month = input(f"Month [{now.month}]: ").strip() or str(now.month)
            try:
                monthly_report(int(year), int(month))
            except ValueError:
                print("Invalid year or month.")

        elif choice == "0":
            t = run_report_in_background()
            t.join(timeout=5)
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Enter 0-8.")


if __name__ == "__main__":
    main()
