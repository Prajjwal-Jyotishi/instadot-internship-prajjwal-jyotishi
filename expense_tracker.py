"""

Day-04  PERSONAL EXPENSE TRACKER

"""

import json
import os
import datetime

# --------------------------------------------------
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


# ──────────────────────────────────────────────────
#  Flat-File Database  (JSON persistence)
# ──────────────────────────────────────────────────

def load_transactions():
    """Read the ledger from the JSON flat-file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Warning: data file unreadable. Starting fresh.")
        return []


def save_transactions(transactions):
    """Write the full ledger back to the JSON flat-file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(transactions, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error saving data: {e}")


# ──────────────────────────────────────────────────
#  Transaction Recording Engine
# ──────────────────────────────────────────────────

def record_salary(transactions):
    """Record an incoming salary / income payload."""
    print("\n--- Add Salary / Income ---")
    try:
        amount = float(input("Enter salary amount (Rs.): "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        source = input("Source (e.g. Company, Freelance): ").strip() or "Salary"
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
        print(f"\n  Income of Rs.{amount:,.2f} recorded successfully.")

    except ValueError as e:
        print(f"  Invalid input: {e}")


def record_expense(transactions):
    """Record a debit expense under a chosen category."""
    print("\n--- Add Expense ---")
    print("  Select a category:")
    for i, cat in enumerate(EXPENSE_CATEGORIES, start=1):
        print(f"    {i}. {cat}")

    try:
        cat_choice = int(input("  Enter category number: "))
        if not (1 <= cat_choice <= len(EXPENSE_CATEGORIES)):
            raise ValueError("Category number out of range.")

        category    = EXPENSE_CATEGORIES[cat_choice - 1]
        amount      = float(input(f"  Enter amount (Rs.) [{category}]: "))

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        description = input("  Description: ").strip() or category

        entry = {
            "type"       : "expense",
            "category"   : category,
            "amount"     : round(amount, 2),
            "description": description,
            "date"       : datetime.date.today().isoformat(),
        }

        transactions.append(entry)
        save_transactions(transactions)
        print(f"\n  Expense of Rs.{amount:,.2f} under '{category}' recorded.")

    except ValueError as e:
        print(f"  Invalid input: {e}")


# ──────────────────────────────────────────────────
#  Automated Ledger Processing
# ──────────────────────────────────────────────────

def parse_monthly_summary(transactions):
    """Parse ledger entries and extract monthly income/expense totals."""
    monthly = {}
    for t in transactions:
        key = t["date"][:7]   # YYYY-MM
        if key not in monthly:
            monthly[key] = {"income": 0.0, "expenses": 0.0}
        if t["type"] == "income":
            monthly[key]["income"] += t["amount"]
        else:
            monthly[key]["expenses"] += t["amount"]
    return monthly


def show_monthly_savings(transactions):
    """Display automatically computed monthly savings balances."""
    if not transactions:
        print("\n  No transactions recorded yet.")
        return

    monthly = parse_monthly_summary(transactions)

    print("\n" + "=" * 54)
    print("         MONTHLY SAVINGS SUMMARY")
    print("=" * 54)
    print(f"  {'Month':<10} {'Income':>12} {'Expenses':>12} {'Savings':>12}")
    print("  " + "-" * 50)

    for month, data in sorted(monthly.items()):
        income   = data["income"]
        expenses = data["expenses"]
        savings  = income - expenses
        status   = "SAVED" if savings >= 0 else "DEFICIT"
        print(f"  {month:<10} Rs.{income:>9,.2f} Rs.{expenses:>9,.2f} Rs.{savings:>9,.2f}  [{status}]")

    print("=" * 54)


# ──────────────────────────────────────────────────
#  Categorical Data Reporting
# ──────────────────────────────────────────────────

def show_category_report(transactions):
    """Aggregate debit counts per category and print the report."""
    expenses = [t for t in transactions if t["type"] == "expense"]

    if not expenses:
        print("\n  No expense records to report.")
        return

    totals = {}
    for t in expenses:
        cat = t["category"]
        totals[cat] = totals.get(cat, 0.0) + t["amount"]

    grand_total = sum(totals.values())

    print("\n" + "=" * 56)
    print("        CATEGORY-WISE EXPENSE REPORT")
    print("=" * 56)
    print(f"  {'Category':<20} {'Amount':>12} {'Share':>8}")
    print("  " + "-" * 52)

    for cat, amt in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        pct = (amt / grand_total * 100) if grand_total else 0
        bar = "#" * int(pct / 5)
        print(f"  {cat:<20} Rs.{amt:>9,.2f} {pct:>6.1f}%  {bar}")

    print("  " + "-" * 52)
    print(f"  {'TOTAL':<20} Rs.{grand_total:>9,.2f}")
    print("=" * 56)


# ──────────────────────────────────────────────────
#  View Full Ledger
# ──────────────────────────────────────────────────

def view_all_transactions(transactions):
    """Print all ledger entries in a clean table."""
    if not transactions:
        print("\n  No transactions found.")
        return

    print("\n" + "=" * 68)
    print("               FULL TRANSACTION LEDGER")
    print("=" * 68)
    print(f"  {'#':<4} {'Date':<12} {'Type':<9} {'Category':<20} {'Amount':>14}")
    print("  " + "-" * 62)

    for i, t in enumerate(transactions, start=1):
        sign     = "+" if t["type"] == "income" else "-"
        category = t.get("category", "-")
        print(f"  {i:<4} {t['date']:<12} {t['type'].upper():<9} {category:<20} {sign}Rs.{t['amount']:>9,.2f}")

    print("=" * 68)
    print(f"  Total entries: {len(transactions)}")


# ──────────────────────────────────────────────────
#  Main Menu
# ──────────────────────────────────────────────────

def main():
    transactions = load_transactions()

    while True:
        print("\n" + "=" * 42)
        print("    PERSONAL EXPENSE TRACKER  (Rs.)")
        print("=" * 42)
        print("  1. Add Salary / Income")
        print("  2. Add Expense")
        print("  3. View All Transactions")
        print("  4. Monthly Savings Summary")
        print("  5. Category-wise Expense Report")
        print("  6. Exit")
        print("-" * 42)

        choice = input("  Select option (1-6): ").strip()

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
            print("\n  Goodbye! Your data has been saved.\n")
            break
        else:
            print("  Invalid option. Please enter 1-6.")


if __name__ == "__main__":
    main()
