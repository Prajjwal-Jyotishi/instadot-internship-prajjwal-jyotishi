# Employee Payroll Management System

## About

This is a simple Python project that helps manage employee payroll records. It allows users to register employees, calculate salaries, search employee details, and generate payroll reports.

## Features

* Employee Registration
* Gross Salary Calculation
* Net Salary Calculation
* Store employee data in JSON format
* Search employee by ID
* Generate payroll summary
* Export payroll report to CSV

## Salary Calculation

**Gross Salary**

```text
Gross Salary = Basic Salary + Bonus
```

**Net Salary**

```text
Net Salary = Gross Salary - Deductions
```

## Technologies Used

* Python
* JSON
* CSV

## Project Structure

```text
EmployeePayrollManagement/
│
├── payroll.py
├── employees.json
├── payroll_report.csv
└── README.md
```

## How to Run

1. Open the project folder.
2. Run the Python file:

```bash
python payroll.py
```

## Menu

```text
1. Register Employee
2. Search Employee
3. Payroll Summary
4. Export Payroll Report
5. Exit
```

## Sample Employee

```text
Employee ID: E101
Name: Rahul
Basic Salary: 30000
Bonus: 5000
Deductions: 2000
```

## Files Generated

* `employees.json` – Stores employee records.
* `payroll_report.csv` – Stores payroll data in CSV format.


