import csv, os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.csv")
RESULTS_FILE = os.path.join(DATA_DIR, "results.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def load_questions():
    if not os.path.exists(QUESTIONS_FILE):
        return []
    with open(QUESTIONS_FILE, newline="") as f:
        return list(csv.DictReader(f))


def save_result(result):
    file_exists = os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["student_id", "name", "score", "total", "percentage", "time_taken", "date"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(result)


def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []
    with open(RESULTS_FILE, newline="") as f:
        return list(csv.DictReader(f))
