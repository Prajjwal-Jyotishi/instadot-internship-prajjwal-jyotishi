import json, os, logging

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.json")
TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.json")

os.makedirs(DATA_DIR, exist_ok=True)


def load(filepath):
    if not os.path.exists(filepath):
        return {} if filepath.endswith(".json") and "transactions" not in filepath else []
    with open(filepath) as f:
        return json.load(f)


def save(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def setup_logging():
    logging.basicConfig(
        filename=os.path.join(DATA_DIR, "banking.log"),
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
