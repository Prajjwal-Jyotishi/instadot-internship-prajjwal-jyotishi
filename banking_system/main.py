import sys, os
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from storage import setup_logging
from auth import register_user, login_user, change_password
from accounts import create_account, close_account, update_details
from banking import deposit, withdraw, transfer, mini_statement, transaction_history
from reports import daily_transactions, monthly_report, customer_summary

setup_logging()


def auth_menu():
    while True:
        print("\n--- Banking Management System ---")
        print("1. Register\n2. Login\n0. Exit")
        ch = input("\nEnter choice: ").strip()

        if ch == "1":
            u = input("Username: ").strip()
            p = input("Password: ").strip()
            register_user(u, p)

        elif ch == "2":
            u = input("Username: ").strip()
            p = input("Password: ").strip()
            if login_user(u, p):
                return u

        elif ch == "0":
            print("Goodbye!")
            sys.exit()

        else:
            print("Invalid choice.")


def main_menu(username):
    while True:
        print(f"\n--- Banking System ({username}) ---")
        print("1. Deposit\n2. Withdraw\n3. Transfer\n4. Mini Statement")
        print("5. Transaction History\n6. Create Account\n7. Close Account")
        print("8. Update Details\n9. Daily Report\n10. Monthly Report")
        print("11. Customer Summary\n12. Change Password\n0. Logout")

        ch = input("\nEnter choice: ").strip()

        try:
            if ch == "1":
                deposit(input("Account ID: ").strip(), float(input("Amount: ").strip()))

            elif ch == "2":
                withdraw(input("Account ID: ").strip(), float(input("Amount: ").strip()))

            elif ch == "3":
                transfer(input("From Account: ").strip(), input("To Account: ").strip(),
                         float(input("Amount: ").strip()))

            elif ch == "4":
                mini_statement(input("Account ID: ").strip())

            elif ch == "5":
                transaction_history(input("Account ID: ").strip())

            elif ch == "6":
                name = input("Account Holder Name: ").strip()
                acc_type = input("Account Type (savings/current): ").strip()
                dep = float(input("Initial Deposit: ").strip())
                create_account(username, name, acc_type, dep)

            elif ch == "7":
                aid = input("Account ID: ").strip()
                if input(f"Close account {aid}? (yes/no): ").strip().lower() == "yes":
                    close_account(aid)
                else:
                    print("Cancelled.")

            elif ch == "8":
                aid = input("Account ID: ").strip()
                field = input("Field to update (name/type): ").strip()
                value = input("New value: ").strip()
                update_details(aid, field, value)

            elif ch == "9":
                date = input("Date (YYYY-MM-DD) [blank=today]: ").strip()
                if not date:
                    date = datetime.now().strftime("%Y-%m-%d")
                daily_transactions(date)

            elif ch == "10":
                now = datetime.now()
                y = input(f"Year [{now.year}]: ").strip() or str(now.year)
                m = input(f"Month [{now.month}]: ").strip() or str(now.month)
                monthly_report(int(y), int(m))

            elif ch == "11":
                customer_summary(input("Account ID: ").strip())

            elif ch == "12":
                old = input("Old Password: ").strip()
                new = input("New Password: ").strip()
                change_password(username, old, new)

            elif ch == "0":
                print("Logged out.")
                return

            else:
                print("Invalid choice. Enter 0-12.")

        except ValueError:
            print("Invalid input.")


def main():
    while True:
        user = auth_menu()
        main_menu(user)


if __name__ == "__main__":
    main()
