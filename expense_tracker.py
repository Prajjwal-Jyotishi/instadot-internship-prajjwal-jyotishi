# Day 04 - Personal Expense Tracker
# Instadot Analytics Internship - Prajjwal Jyotishi
#
# Features:
# 1. Record salary/income and expenses
# 2. Save all data to a JSON file (persistent storage)
# 3. Show monthly savings summary
# 4. Show category-wise expense report

import json
import os
import datetime

DATA_FILE = "transactions.json"

categories = [
    "Food & Dining",
    "Rent & Housing",
    "Transport",
    "Shopping",
    "Healthcare",
    "Entertainment",
    "Education",
    "Utilities",
    "Other"
]


# Load saved transactions from the JSON file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        print("Could not load data. Starting fresh.")
        return []


# Save all transactions to the JSON file
def save_data(transactions):
    with open(DATA_FILE, "w") as f:
        json.dump(transactions, f, indent=4)


# Add a salary or income entry
def add_income(transactions):
    print("\n--- Add Income / Salary ---")
    try:
        amount = float(input("Enter amount (Rs.): "))
        if amount <= 0:
            print("Amount should be more than 0.")
            return

        source = input("Source (Company / Freelance etc.): ").strip()
        if not source:
            source = "Salary"

        note = input("Any note (optional): ").strip()
        today = datetime.date.today().isoformat()

        entry = {
            "type": "income",
            "category": "Salary",
            "amount": round(amount, 2),
            "source": source,
            "note": note,
            "date": today
        }

        transactions.append(entry)
        save_data(transactions)
        print(f"Income of Rs.{amount:.2f} added successfully!")

    except ValueError:
        print("Please enter a valid number.")


# Add an expense entry
def add_expense(transactions):
    print("\n--- Add Expense ---")
    print("Select category:")
    for i, cat in enumerate(categories, start=1):
        print(f"  {i}. {cat}")

    try:
        choice = int(input("Enter category number: "))
        if choice < 1 or choice > len(categories):
            print("Invalid category number.")
            return

        cat = categories[choice - 1]
        amount = float(input(f"Enter amount (Rs.) for {cat}: "))

        if amount <= 0:
            print("Amount should be more than 0.")
            return

        desc = input("Description (optional): ").strip()
        if not desc:
            desc = cat

        today = datetime.date.today().isoformat()

        entry = {
            "type": "expense",
            "category": cat,
            "amount": round(amount, 2),
            "description": desc,
            "date": today
        }

        transactions.append(entry)
        save_data(transactions)
        print(f"Expense of Rs.{amount:.2f} under '{cat}' added!")

    except ValueError:
        print("Please enter a valid number.")


# Show all recorded transactions
def show_all(transactions):
    if not transactions:
        print("\nNo transactions yet.")
        return

    print("\n" + "-" * 60)
    print("           ALL TRANSACTIONS")
    print("-" * 60)
    print(f"{'No.':<5} {'Date':<12} {'Type':<10} {'Category':<20} {'Amount'}")
    print("-" * 60)

    for i, t in enumerate(transactions, start=1):
        sign = "+" if t["type"] == "income" else "-"
        print(f"{i:<5} {t['date']:<12} {t['type'].upper():<10} {t['category']:<20} {sign}Rs.{t['amount']:.2f}")

    print("-" * 60)
    print(f"Total records: {len(transactions)}")


# Calculate and show monthly savings
def show_monthly_savings(transactions):
    if not transactions:
        print("\nNo transactions to process.")
        return

    # Group data by month (YYYY-MM)
    monthly = {}
    for t in transactions:
        month = t["date"][:7]
        if month not in monthly:
            monthly[month] = {"income": 0, "expenses": 0}
        if t["type"] == "income":
            monthly[month]["income"] += t["amount"]
        else:
            monthly[month]["expenses"] += t["amount"]

    print("\n" + "-" * 55)
    print("          MONTHLY SAVINGS SUMMARY")
    print("-" * 55)
    print(f"{'Month':<12} {'Income':>12} {'Expenses':>12} {'Savings':>12}")
    print("-" * 55)

    for month in sorted(monthly):
        income = monthly[month]["income"]
        expenses = monthly[month]["expenses"]
        savings = income - expenses
        status = "SAVED" if savings >= 0 else "DEFICIT"
        print(f"{month:<12} Rs.{income:>8.2f} Rs.{expenses:>8.2f} Rs.{savings:>8.2f}  ({status})")

    print("-" * 55)


# Show total spending per category
def show_category_report(transactions):
    expenses = [t for t in transactions if t["type"] == "expense"]

    if not expenses:
        print("\nNo expenses recorded yet.")
        return

    # Add up amounts per category
    totals = {}
    for t in expenses:
        cat = t["category"]
        if cat not in totals:
            totals[cat] = 0
        totals[cat] += t["amount"]

    grand_total = sum(totals.values())

    print("\n" + "-" * 50)
    print("       CATEGORY-WISE EXPENSE REPORT")
    print("-" * 50)
    print(f"{'Category':<22} {'Amount':>10} {'%':>8}")
    print("-" * 50)

    # Sort by highest spending first
    for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / grand_total) * 100
        print(f"{cat:<22} Rs.{amt:>7.2f} {pct:>7.1f}%")

    print("-" * 50)
    print(f"{'TOTAL':<22} Rs.{grand_total:>7.2f}")
    print("-" * 50)


# Main menu
def main():
    transactions = load_data()

    while True:
        print("\n==============================")
        print("   PERSONAL EXPENSE TRACKER")
        print("==============================")
        print("1. Add Salary / Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. Monthly Savings Summary")
        print("5. Category-wise Report")
        print("6. Exit")
        print("------------------------------")

        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            add_income(transactions)
        elif choice == "2":
            add_expense(transactions)
        elif choice == "3":
            show_all(transactions)
        elif choice == "4":
            show_monthly_savings(transactions)
        elif choice == "5":
            show_category_report(transactions)
        elif choice == "6":
            print("\nBye! Your data is saved.")
            break
        else:
            print("Invalid choice. Please pick 1 to 6.")


main()
