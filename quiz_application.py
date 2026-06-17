import json, random

with open("questions.json", "r") as f:
    questions = json.load(f)

random.shuffle(questions)
score = 0
total = len(questions)

print("\n===== WELCOME TO THE QUIZ =====\n")

for i, q in enumerate(questions, 1):
    print(f"Q{i}: {q['question']}")
    for option in q["options"]:
        print(f"  {option}")
    while True:
        try:
            answer = input("Your answer (A/B/C/D): ").strip().upper()
            if answer not in ["A", "B", "C", "D"]:
                raise ValueError("Invalid input! Please enter A, B, C, or D.")
            break
        except ValueError as e:
            print(f"Error: {e}")
    if answer == q["answer"]:
        print("Correct!\n")
        score += 1
    else:
        print(f"Wrong! Correct answer: {q['answer']}\n")

print("===== QUIZ FINISHED =====")
print(f"Your Score: {score}/{total}")

percentage = (score / total) * 100
if percentage == 100:
    print("Performance: Excellent!")
elif percentage >= 60:
    print("Performance: Good!")
elif percentage >= 40:
    print("Performance: Average!")
else:
    print("Performance: Poor! Keep practicing.")
