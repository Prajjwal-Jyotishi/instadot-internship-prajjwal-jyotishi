import random, time
from datetime import datetime
from storage import load_questions, save_result, load_results

TIME_LIMIT = 300  # 5 minutes total exam time


def student_login():
    print("\n--- Student Login ---")
    sid = input("Student ID: ").strip()
    name = input("Name: ").strip()
    if not sid or not name:
        print("ID and Name cannot be empty.")
        return None, None
    print(f"Welcome, {name}!")
    return sid, name


def run_exam(sid, name):
    questions = load_questions()
    if not questions:
        print("No questions found. Add questions to data/questions.csv")
        return

    random.shuffle(questions)  # Bonus: randomize question order every attempt

    score = 0
    total = len(questions)
    start = time.time()

    print(f"\nExam started! You have {TIME_LIMIT // 60} minutes for {total} questions.")
    print("Answer with A, B, C, or D.\n")

    for i, q in enumerate(questions):
        remaining = int(TIME_LIMIT - (time.time() - start))
        if remaining <= 0:
            print("\nTime's up! Auto-submitting...")
            break

        print(f"Q{i + 1}/{total}  [Time left: {remaining // 60}m {remaining % 60}s]\n"
              f"{q['question']}\n"
              f"  A. {q['option_a']}\n  B. {q['option_b']}\n"
              f"  C. {q['option_c']}\n  D. {q['option_d']}")

        ans = input("Answer (A/B/C/D): ").strip().upper()
        if ans not in ("A", "B", "C", "D"):
            print("Invalid input, marked wrong.\n")
            continue

        if ans == q["answer"].strip().upper():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong! Correct answer: {q['answer'].strip()}\n")

    time_taken = round(time.time() - start, 1)
    percentage = round(score / total * 100, 1)

    result = {
        "student_id": sid,
        "name": name,
        "score": score,
        "total": total,
        "percentage": percentage,
        "time_taken": f"{time_taken}s",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    save_result(result)

    print(f"\n{'=' * 40}\n  Result Summary\n{'=' * 40}\n"
          f"  Name      : {name}\n"
          f"  Score     : {score}/{total}\n  Percentage: {percentage}%\n"
          f"  Time Taken: {time_taken}s\n"
          f"  Grade     : {'PASS' if percentage >= 50 else 'FAIL'}\n"
          f"{'=' * 40}\nResult saved to data/results.csv")


def view_my_results(sid):
    results = [r for r in load_results() if r["student_id"] == sid]
    if not results:
        print(f"No results found for ID '{sid}'.")
        return
    print(f"\n{'=' * 55}\n  Results for Student ID: {sid}\n{'=' * 55}\n"
          f"{'#':<4} {'Score':<8} {'%':<8} {'Time':<12} {'Date'}\n" + "-" * 55)
    for i, r in enumerate(results, 1):
        print(f"{i:<4} {r['score']}/{r['total']:<6} {r['percentage']:<8} {r['time_taken']:<12} {r['date']}")


def view_all_results():
    results = load_results()
    if not results:
        print("No results yet.")
        return
    print(f"\n{'=' * 65}\n  All Exam Results\n{'=' * 65}\n"
          f"{'ID':<12} {'Name':<20} {'Score':<8} {'%':<8} {'Date'}\n" + "-" * 65)
    for r in results:
        print(f"{r['student_id']:<12} {r['name']:<20} {r['score']}/{r['total']:<6} {r['percentage']:<8} {r['date']}")
