import sys
from system import student_login, run_exam, view_my_results, view_all_results

def main():
    current_sid = None
    current_name = None

    while True:
        print("\n--- Online Examination System ---")
        if current_sid:
            print(f"Logged in as: {current_name} ({current_sid})")
            print("1. Take Exam")
            print("2. View My Results")
            print("3. Logout")
        else:
            print("1. Student Login")
            print("2. View All Results (Admin)")

        print("0. Exit")

        choice = input("\nEnter choice: ").strip()

        if choice == '0':
            print("Goodbye!")
            break

        if current_sid:
            if choice == '1':
                run_exam(current_sid, current_name)
            elif choice == '2':
                view_my_results(current_sid)
            elif choice == '3':
                current_sid = None
                current_name = None
                print("Logged out successfully.")
            else:
                print("Invalid choice.")
        else:
            if choice == '1':
                current_sid, current_name = student_login()
            elif choice == '2':
                view_all_results()
            else:
                print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)
