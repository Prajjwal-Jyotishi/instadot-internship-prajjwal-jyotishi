
import json
import csv
import os

FILE_NAME = "employees.json"


# Load employee data
def load_employees():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


# Save employee data
def save_employees(employees):
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


# Employee Registration
def register_employee():
    employees = load_employees()

    emp_id = input("Enter Employee ID: ")
    
    # Check if employee ID already exists
    if any(emp["ID"] == emp_id for emp in employees):
        print(f"Employee ID '{emp_id}' already exists!")
        return

    name = input("Enter Employee Name: ")
    
    try:
        basic_salary = float(input("Enter Basic Salary: "))
        bonus = float(input("Enter Bonus: "))
        deductions = float(input("Enter Deductions: "))
    except ValueError:
        print("Invalid input! Please enter numeric values for salary, bonus, and deductions.")
        return

    gross_salary = basic_salary + bonus
    net_salary = gross_salary - deductions

    employee = {
        "ID": emp_id,
        "Name": name,
        "Basic Salary": basic_salary,
        "Bonus": bonus,
        "Deductions": deductions,
        "Gross Salary": gross_salary,
        "Net Salary": net_salary
    }

    employees.append(employee)
    save_employees(employees)

    print("\nEmployee Registered Successfully!")


# Search Employee by ID
def search_employee():
    employees = load_employees()

    emp_id = input("Enter Employee ID to Search: ")

    for employee in employees:
        if employee["ID"] == emp_id:
            print("\nEmployee Found")
            print("----------------")
            for key, value in employee.items():
                print(f"{key}: {value}")
            return

    print("Employee not found.")


# Generate Payroll Summary
def payroll_summary():
    employees = load_employees()

    if not employees:
        print("No employee records found.")
        return

    total_gross = sum(emp["Gross Salary"] for emp in employees)
    total_net = sum(emp["Net Salary"] for emp in employees)

    print("\nPayroll Summary")
    print("----------------")
    print("Total Employees :", len(employees))
    print("Total Gross Salary :", total_gross)
    print("Total Net Salary :", total_net)


# Export Payroll Report to CSV
def export_csv():
    employees = load_employees()

    if not employees:
        print("No data available to export.")
        return

    with open("payroll_report.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=employees[0].keys())
        writer.writeheader()
        writer.writerows(employees)

    print("Payroll report exported successfully.")


# Main Menu
def main():
    while True:
        print("\n===== Employee Payroll Management System =====")
        print("1. Register Employee")
        print("2. Search Employee")
        print("3. Payroll Summary")
        print("4. Export Payroll Report")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register_employee()

        elif choice == "2":
            search_employee()

        elif choice == "3":
            payroll_summary()

        elif choice == "4":
            export_csv()

        elif choice == "5":
            print("Thank you!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
