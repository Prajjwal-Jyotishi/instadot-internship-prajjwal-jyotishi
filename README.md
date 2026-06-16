# Day 05 – Employee Payroll Management System

## Objective

Develop a menu-driven Employee Payroll Management System in Python to manage employee salary records by registering employees, calculating salaries, searching records, generating payroll summaries, and exporting reports using JSON file persistence.

## Features Implemented

### Employee Registration

* Register new employees with the following details:

  * Employee ID
  * Employee Name
  * Basic Salary
  * Bonus
  * Deductions

* Automatically calculates:

  * Gross Salary
  * Net Salary

* Prevents duplicate Employee IDs

### Employee Search

* Search and retrieve employee details by Employee ID
* Displays all stored information for the matched employee

### Payroll Summary

* Displays total number of registered employees
* Calculates and displays total gross salary
* Calculates and displays total net salary

### Payroll Report Export

* Exports all employee records to a CSV file
* Report includes all salary fields for each employee

### Data Persistence

* Stores all employee records in a JSON file
* Loads existing data automatically on application startup
* Saves updates after every registration

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

* Python 3
* JSON File Handling
* CSV File Handling
* Functions and Modular Programming
* Exception Handling
* Lists and Dictionaries

## Files Included

### employee_payroll_management_system.py

Main application file containing:

* Employee registration logic
* Salary calculation functions
* Search functionality
* Payroll summary generation
* CSV export feature
* Menu-driven interface

### employees.json

JSON file used to store all employee records persistently.

### payroll_report.csv

CSV file generated when the export option is selected from the menu.

## Functionalities

### Register Employee

Allows users to add a new employee with salary details. Validates that the Employee ID is unique and all numeric inputs are valid.

### Search Employee

Allows users to search for an employee by their ID and view all their salary details.

### Payroll Summary

Displays aggregate payroll data including total number of employees and total gross and net salary.

### Export Payroll Report

Exports all employee records into a CSV file named payroll_report.csv.

## Learning Outcomes

Through this project, the following concepts were practiced:

* Python Functions
* File Handling
* JSON Serialization
* CSV Writing
* Data Structures (Lists and Dictionaries)
* Exception Handling
* Modular Programming
* Payroll Data Processing
