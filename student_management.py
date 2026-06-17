students = []

def add_student():
    try:
        student_id = int(input("Enter Student ID: "))
        name = input("Enter Student Name: ")
        age = int(input("Enter Student Age: "))

        student = {
            "id": student_id,
            "name": name,
            "age": age
        }

        students.append(student)
        print("Student added successfully!")

    except ValueError:
        print("Invalid input! Please enter numbers where required.")


def view_students():
    if len(students) == 0:
        print("No students found.")
    else:
        print("\nStudent Records:")
        for student in students:
            print(student)


def update_student():
    try:
        student_id = int(input("Enter Student ID to update: "))

        for student in students:
            if student["id"] == student_id:
                student["name"] = input("Enter New Name: ")
                student["age"] = int(input("Enter New Age: "))
                print("Student updated successfully!")
                return

        print("Student not found.")

    except ValueError:
        print("Invalid input!")


def delete_student():
    try:
        student_id = int(input("Enter Student ID to delete: "))

        for student in students:
            if student["id"] == student_id:
                students.remove(student)
                print("Student deleted successfully!")
                return

        print("Student not found.")

    except ValueError:
        print("Invalid input!")


def search_student():
    name = input("Enter name to search: ").lower()

    found = False

    for student in students:
        if name in student["name"].lower():
            print(student)
            found = True

    if not found:
        print("No matching student found.")


def filter_students():
    try:
        min_age = int(input("Show students with age greater than or equal to: "))

        found = False

        for student in students:
            if student["age"] >= min_age:
                print(student)
                found = True

        if not found:
            print("No students match the filter.")

    except ValueError:
        print("Invalid age entered.")


while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Search Student")
    print("6. Filter Students")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_student()

    elif choice == "2":
        view_students()

    elif choice == "3":
        update_student()

    elif choice == "4":
        delete_student()

    elif choice == "5":
        search_student()

    elif choice == "6":
        filter_students()

    elif choice == "7":
        print("Thank you!")
        break

    else:
        print("Invalid choice. Please try again.")