import sys
from system import student_login, run_exam, view_my_results, view_all_results

def main():
    current_sid = None
    current_name = None

    while True:
        if current_sid:
            print(f"\n--- Online Examination System ---\nLogged in as: {current_name} ({current_sid})\n"
                  f"1. Take Exam\n2. View My Results\n3. Logout\n0. Exit")
        else:
            print(f"\n--- Online Examination System ---\n1. Student Login\n"
                  f"2. View All Results (Admin)\n0. Exit")

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
