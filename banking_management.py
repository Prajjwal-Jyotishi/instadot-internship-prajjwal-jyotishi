"""
Day 03 - Banking Management System
"""

balance = 0.0
transaction_history = []

def deposit():
    global balance, transaction_history
    try:
        amount = float(input("Enter amount to deposit: $"))
        if amount <= 0:
            print("Error: Deposit amount must be greater than zero.")
            return
        
        balance += amount
        transaction_history.append(f"Deposited: ${amount:.2f}")
        print(f"Successfully deposited ${amount:.2f}.")
    except ValueError:
        print("Invalid input! Please enter a valid numerical amount.")

def withdraw():
    global balance, transaction_history
    try:
        amount = float(input("Enter amount to withdraw: $"))
        if amount <= 0:
            print("Error: Withdrawal amount must be greater than zero.")
            return
        
        if amount > balance:
            print("Insufficient funds! Transaction denied.")
            return
            
        balance -= amount
        transaction_history.append(f"Withdrew: ${amount:.2f}")
        print(f"Successfully withdrew ${amount:.2f}.")
    except ValueError:
        print("Invalid input! Please enter a valid numerical amount.")

def check_balance():
    global balance
    print(f"\nCurrent Account Balance: ${balance:.2f}")

def view_history():
    global transaction_history
    print("\n--- Transaction History ---")
    if not transaction_history:
        print("No transactions have been made yet.")
    else:
        for index, transaction in enumerate(transaction_history, 1):
            print(f"{index}. {transaction}")
    print("---------------------------")

def main():
    while True:
        print("\n*** Banking Management System ***")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Account Balance")
        print("4. View Transaction History")
        print("5. Exit")
        
        choice = input("Please select an option (1-5): ")
        
        if choice == '1':
            deposit()
        elif choice == '2':
            withdraw()
        elif choice == '3':
            check_balance()
        elif choice == '4':
            view_history()
        elif choice == '5':
            print("Thank you for using the Banking Management System. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a number between 1 and 5.")

if __name__ == "__main__":
    main()
