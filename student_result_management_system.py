import json, csv, os

subjects = ["Math", "Science", "English", "Hindi", "Computer"]


def load_data():
    if not os.path.exists("students.json"):
        return []
    file = open("students.json")
    data = json.load(file)
    file.close()
    return data


def save_data(data):
    file = open("students.json", "w")
    json.dump(data, file, indent=4)
    file.close()


def get_grade(p):
    if p >= 90: return "A+"
    if p >= 80: return "A"
    if p >= 70: return "B"
    if p >= 60: return "C"
    if p >= 50: return "D"
    return "F"


def register():
    data = load_data()
    name = input("Enter Student Name: ")
    roll = input("Enter Roll Number: ")

    for s in data:
        if s["roll"] == roll:
            print("Roll Number already exists!\n")
            return

    marks = {}
    print("Enter marks (0-100):")
    for sub in subjects:
        while True:
            try:
                m = int(input("  " + sub + ": "))
                if 0 <= m <= 100:
                    marks[sub] = m
                    break
                else:
                    print("  Enter between 0 and 100.")
            except ValueError:
                print("  Enter a valid number.")

    total = sum(marks.values())
    per = total / 5

    data.append({"name": name, "roll": roll, "marks": marks,
                 "total": total, "percentage": per, "grade": get_grade(per)})
    save_data(data)
    print("Student registered!\n")


def search():
    data = load_data()
    roll = input("Enter Roll Number: ")

    for s in data:
        if s["roll"] == roll:
            print("\n  Name       :", s["name"])
            print("  Roll No    :", s["roll"])
            for sub in subjects:
                print("  " + sub.ljust(10) + ":", s["marks"][sub])
            print("  Total      :", s["total"], "/ 500")
            print("  Percentage :", s["percentage"], "%")
            print("  Grade      :", s["grade"], "\n")
            return

    print("Student not found.\n")


def display_all():
    data = load_data()
    if not data:
        print("No students registered.\n")
        return

    print("\nName            Roll     Total   %       Grade")
    print("-" * 50)
    for s in data:
        print(s["name"].ljust(16), s["roll"].ljust(8),
              str(s["total"]).ljust(7), str(s["percentage"]).ljust(7), s["grade"])
    print()


def export_csv():
    data = load_data()
    if not data:
        print("No students to export.\n")
        return

    file = open("result_report.csv", "w", newline="")
    writer = csv.writer(file)
    writer.writerow(["Name", "Roll No"] + subjects + ["Total", "Percentage", "Grade"])
    for s in data:
        row = [s["name"], s["roll"]]
        for sub in subjects:
            row.append(s["marks"][sub])
        row += [s["total"], s["percentage"], s["grade"]]
        writer.writerow(row)
    file.close()
    print("Exported to result_report.csv!\n")


# Main Menu
while True:
    print("===== Student Result Management System =====")
    print("1. Register Student")
    print("2. Search by Roll Number")
    print("3. Display All Results")
    print("4. Export to CSV")
    print("5. Exit")
    ch = input("Enter choice (1-5): ")
    if ch == "1":   register()
    elif ch == "2": search()
    elif ch == "3": display_all()
    elif ch == "4": export_csv()
    elif ch == "5": print("Goodbye!"); break
    else: print("Invalid choice.\n")
