"""
students.py — Student Registration, Search, List, Delete.
"""

from storage import load_students, save_students


def register_student(student_id: str, name: str, course: str) -> str:
    students = load_students()
    if student_id in students:
        return f"[ERROR] Student ID '{student_id}' already exists."
    students[student_id] = {"name": name, "course": course}
    save_students(students)
    return f"[OK] Student '{name}' registered with ID '{student_id}'."


def search_student(student_id: str) -> dict | None:
    return load_students().get(student_id)


def list_students() -> dict:
    return load_students()


def delete_student(student_id: str) -> str:
    students = load_students()
    if student_id not in students:
        return f"[ERROR] Student ID '{student_id}' not found."
    name = students.pop(student_id)["name"]
    save_students(students)
    return f"[OK] Student '{name}' (ID: {student_id}) deleted."
