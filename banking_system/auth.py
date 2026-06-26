import hashlib, logging
from storage import load, save, USERS_FILE


def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password):
    users = load(USERS_FILE)
    if username in users:
        print(f"Username '{username}' already exists.")
        return False
    users[username] = {"password": hash_pw(password), "accounts": []}
    save(USERS_FILE, users)
    logging.info(f"User '{username}' registered")
    print(f"User '{username}' registered successfully.")
    return True


def login_user(username, password):
    users = load(USERS_FILE)
    if username not in users:
        print("Invalid username.")
        return False
    if users[username]["password"] != hash_pw(password):
        print("Incorrect password.")
        return False
    logging.info(f"User '{username}' logged in")
    print(f"Welcome, {username}!")
    return True


def change_password(username, old_pw, new_pw):
    users = load(USERS_FILE)
    if users[username]["password"] != hash_pw(old_pw):
        print("Old password incorrect.")
        return
    users[username]["password"] = hash_pw(new_pw)
    save(USERS_FILE, users)
    logging.info(f"User '{username}' changed password")
    print("Password changed successfully.")
