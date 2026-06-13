balance = 0
transaction_history = []


def deposit():
    global balance

    try:
        amount = float(input("Enter amount to deposit: "))

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        balance += amount
        transaction_history.append(f"Deposited ₹{amount}")

        print("Deposit successful!")

    except ValueError as e:
        print("Error:", e)


def withdraw():
    global balance

    try:
        amount = float(input("Enter amount to withdraw: "))

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        if amount > balance:
            raise ValueError("Insufficient balance.")

        balance -= amount
        transaction_history.append(f"Withdrawn ₹{amount}")

        print("Withdrawal successful!")

    except ValueError as e:
        print("Error:", e)


def check_balance():
    print(f"Current Balance: ₹{balance}")


def show_transaction_history():

    if not transaction_history:
        print("No transactions found.")
        return

    print("\nTransaction History")

    for transaction in transaction_history:
        print(transaction)


def main():

    while True:

        print("\n===== Banking Management System =====")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Balance Inquiry")
        print("4. Transaction History")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            deposit()

        elif choice == "2":
            withdraw()

        elif choice == "3":
            check_balance()

        elif choice == "4":
            show_transaction_history()

        elif choice == "5":
            print("Thank you!")
            break

        else:
            print("Invalid choice.")


main()
