import logging
from datetime import datetime
from storage import load, save, USERS_FILE, ACCOUNTS_FILE

_next_id = 1001


def _gen_id():
    global _next_id
    accounts = load(ACCOUNTS_FILE)
    if accounts:
        _next_id = max(int(k) for k in accounts) + 1
    else:
        _next_id = 1001
    return str(_next_id)


def create_account(username, name, acc_type, deposit):
    if deposit < 0:
        print("Initial deposit cannot be negative.")
        return None
    acc_id = _gen_id()
    accounts = load(ACCOUNTS_FILE)
    accounts[acc_id] = {
        "owner": username, "name": name, "type": acc_type,
        "balance": deposit, "status": "active",
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    save(ACCOUNTS_FILE, accounts)

    users = load(USERS_FILE)
    users[username]["accounts"].append(acc_id)
    save(USERS_FILE, users)

    logging.info(f"Account {acc_id} created for '{username}'")
    print(f"Account created! ID: {acc_id}")
    return acc_id


def close_account(acc_id):
    accounts = load(ACCOUNTS_FILE)
    if acc_id not in accounts:
        print(f"Account '{acc_id}' not found.")
        return
    if accounts[acc_id]["status"] == "closed":
        print("Account already closed.")
        return
    accounts[acc_id]["status"] = "closed"
    accounts[acc_id]["balance"] = 0.0
    save(ACCOUNTS_FILE, accounts)
    logging.info(f"Account {acc_id} closed")
    print(f"Account {acc_id} closed successfully.")


def update_details(acc_id, field, value):
    accounts = load(ACCOUNTS_FILE)
    if acc_id not in accounts:
        print(f"Account '{acc_id}' not found.")
        return
    if field not in ("name", "type"):
        print("Can only update 'name' or 'type'.")
        return
    accounts[acc_id][field] = value
    save(ACCOUNTS_FILE, accounts)
    logging.info(f"Account {acc_id} updated {field} to '{value}'")
    print(f"Account {acc_id} {field} updated to '{value}'.")


def get_account(acc_id):
    accounts = load(ACCOUNTS_FILE)
    return accounts.get(acc_id)
