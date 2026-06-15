"""

Day-04 PERSONAL EXPENSE TRACKER

Features:
 - Record salary (income) and categorised expenses
 - Auto-save every transaction to a JSON flat file
 - Parse the ledger and compute monthly savings
 - Generate a category-wise spending report

"""

import json
import os
import datetime

# ─────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────
DATA_FILE = "transactions.json"

EXPENSE_CATEGORIES = [
    "Food & Dining",
    "Rent & Housing",
    "Transport",
    "Shopping",
    "Healthcare",
    "Entertainment",
    "Education",
    "Utilities",
    "Other",
]


# ─────────────────────────────────────────────
#  Flat-File Database Helpers
# ─────────────────────────────────────────────

def load_transactions():
    """Load transaction ledger from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: could not read data file. Starting fresh.")
        return []


def save_transactions(transactions):
    """Persist the full ledger back to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(transactions, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving data: {e}")


# ─────────────────────────────────────────────
#  Transaction Recording Engine
# ─────────────────────────────────────────────

def record_salary(transactions):
    """Record an incoming salary / income entry."""
    print("\n--- Add Salary / Income ---")
    try:
        amount = float(input("Enter salary amount (₹): "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        source = input("Source (e.g. Company name, Freelance): ").strip() or "Salary"
        note   = input("Note (optional): ").strip()

        entry = {
            "type"    : "income",
            "category": "Salary",
            "amount"  : round(amount, 2),
            "source"  : source,
            "note"    : note,
            "date"    : datetime.date.today().isoformat(),
        }

        transactions.append(entry)
        save_transactions(transactions)
        print(f"\n✓ Income of ₹{amount:,.2f} recorded successfully.")

    except ValueError as e:
        print(f"Invalid input: {e}")


def record_expense(transactions):
    """Record a debit / expense entry under a chosen category."""
    print("\n--- Add Expense ---")
    print("Select a category:")
    for i, cat in enumerate(EXPENSE_CATEGORIES, start=1):
        print(f"  {i}. {cat}")

    try:
        cat_choice = int(input("Enter category number: "))
        if not (1 <= cat_choice <= len(EXPENSE_CATEGORIES)):
            raise ValueError("Category number out of range.")

        category = EXPENSE_CATEGORIES[cat_choice - 1]
        amount   = float(input(f"Enter expense amount (₹) [{category}]: "))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        description = input("Description: ").strip() or category

        entry = {
            "type"       : "expense",
            "category"   : category,
            "amount"     : round(amount, 2),
            "description": description,
            "date"       : datetime.date.today().isoformat(),
        }

        transactions.append(entry)
        save_transactions(transactions)
        print(f"\n✓ Expense of ₹{amount:,.2f} under '{category}' recorded.")

    except ValueError as e:
        print(f"Invalid input: {e}")


# ─────────────────────────────────────────────
#  Automated Ledger Processing
# ─────────────────────────────────────────────

def parse_monthly_summary(transactions):
    """
    Parse the full ledger and compute per-month income,
    total spending, and net savings automatically.
    """
    monthly = {}

    for t in transactions:
        month_key = t["date"][:7]           # 'YYYY-MM'
        if month_key not in monthly:
            monthly[month_key] = {"income": 0.0, "expenses": 0.0}

        if t["type"] == "income":
            monthly[month_key]["income"] += t["amount"]
        else:
            monthly[month_key]["expenses"] += t["amount"]

    return monthly


def show_monthly_savings(transactions):
    """Display computed monthly savings from the ledger."""
    if not transactions:
        print("\nNo transactions recorded yet.")
        return

    monthly = parse_monthly_summary(transactions)

    print("\n" + "=" * 50)
    print("       MONTHLY SAVINGS SUMMARY")
    print("=" * 50)
    print(f"{'Month':<12} {'Income':>12} {'Expenses':>12} {'Savings':>12}")
    print("-" * 50)

    for month, data in sorted(monthly.items()):
        income   = data["income"]
        expenses = data["expenses"]
        savings  = income - expenses
        flag     = "✓" if savings >= 0 else "✗"
        print(f"{month:<12} ₹{income:>10,.2f} ₹{expenses:>10,.2f} ₹{savings:>10,.2f}  {flag}")

    print("=" * 50)


# ─────────────────────────────────────────────
#  Categorical Data Reporting
# ─────────────────────────────────────────────

def show_category_report(transactions):
    """
    Aggregate total spend per category and display
    a structured summary report.
    """
    expense_txns = [t for t in transactions if t["type"] == "expense"]

    if not expense_txns:
        print("\nNo expense records to report.")
        return

    # Aggregate
    category_totals = {}
    for t in expense_txns:
        cat = t["category"]
        category_totals[cat] = category_totals.get(cat, 0.0) + t["amount"]

    total_spent = sum(category_totals.values())

    print("\n" + "=" * 52)
    print("       CATEGORY-WISE EXPENSE REPORT")
    print("=" * 52)
    print(f"{'Category':<22} {'Amount':>12} {'Share %':>10}")
    print("-" * 52)

    for cat, amt in sorted(category_totals.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / total_spent * 100) if total_spent else 0
        bar = "█" * int(pct / 5)          # simple visual bar
        print(f"{cat:<22} ₹{amt:>10,.2f} {pct:>8.1f}%  {bar}")

    print("-" * 52)
    print(f"{'TOTAL EXPENSES':<22} ₹{total_spent:>10,.2f}")
    print("=" * 52)


# ─────────────────────────────────────────────
#  View Full Ledger
# ─────────────────────────────────────────────

def view_all_transactions(transactions):
    """Print every ledger entry in a readable table."""
    if not transactions:
        print("\nNo transactions found.")
        return

    print("\n" + "=" * 70)
    print("                   FULL TRANSACTION LEDGER")
    print("=" * 70)
    print(f"{'#':<4} {'Date':<12} {'Type':<10} {'Category':<22} {'Amount':>12}")
    print("-" * 70)

    for i, t in enumerate(transactions, start=1):
        ttype    = t["type"].upper()
        category = t.get("category", "-")
        amount   = t["amount"]
        sign     = "+" if t["type"] == "income" else "-"
        print(f"{i:<4} {t['date']:<12} {ttype:<10} {category:<22} {sign}₹{amount:>10,.2f}")

    print("=" * 70)
    print(f"Total entries: {len(transactions)}")


# ─────────────────────────────────────────────
#  Main Menu
# ─────────────────────────────────────────────

def main():
    transactions = load_transactions()

    while True:
        print("\n" + "=" * 40)
        print("   PERSONAL EXPENSE TRACKER  (₹)")
        print("=" * 40)
        print("  1. Add Salary / Income")
        print("  2. Add Expense")
        print("  3. View All Transactions")
        print("  4. Monthly Savings Summary")
        print("  5. Category-wise Expense Report")
        print("  6. Exit")
        print("-" * 40)

        choice = input("  Select option: ").strip()

        if choice == "1":
            record_salary(transactions)

        elif choice == "2":
            record_expense(transactions)

        elif choice == "3":
            view_all_transactions(transactions)

        elif choice == "4":
            show_monthly_savings(transactions)

        elif choice == "5":
            show_category_report(transactions)

        elif choice == "6":
            print("\nGoodbye! Your data has been saved.\n")
            break

        else:
            print("Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()
