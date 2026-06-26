import logging
from datetime import datetime
from storage import load, save, ACCOUNTS_FILE, TRANSACTIONS_FILE


def _log_txn(acc_id, txn_type, amount, balance_after, note=""):
    records = load(TRANSACTIONS_FILE)
    if not isinstance(records, list):
        records = []
    records.append({
        "id": len(records) + 1, "account_id": acc_id, "type": txn_type,
        "amount": amount, "balance_after": balance_after,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "note": note
    })
    save(TRANSACTIONS_FILE, records)


def _check_active(acc_id):
    accounts = load(ACCOUNTS_FILE)
    if acc_id not in accounts:
        print(f"Account '{acc_id}' not found.")
        return None
    if accounts[acc_id]["status"] == "closed":
        print("Account is closed.")
        return None
    return accounts


def deposit(acc_id, amount):
    if amount <= 0:
        print("Amount must be positive.")
        return
    accounts = _check_active(acc_id)
    if not accounts:
        return
    accounts[acc_id]["balance"] += amount
    save(ACCOUNTS_FILE, accounts)
    _log_txn(acc_id, "deposit", amount, accounts[acc_id]["balance"])
    logging.info(f"Deposit {amount} to {acc_id}")
    print(f"Deposited {amount:.2f}. Balance: {accounts[acc_id]['balance']:.2f}")


def withdraw(acc_id, amount):
    if amount <= 0:
        print("Amount must be positive.")
        return
    accounts = _check_active(acc_id)
    if not accounts:
        return
    if accounts[acc_id]["balance"] < amount:
        print(f"Insufficient balance. Available: {accounts[acc_id]['balance']:.2f}")
        return
    accounts[acc_id]["balance"] -= amount
    save(ACCOUNTS_FILE, accounts)
    _log_txn(acc_id, "withdraw", amount, accounts[acc_id]["balance"])
    logging.info(f"Withdraw {amount} from {acc_id}")
    print(f"Withdrawn {amount:.2f}. Balance: {accounts[acc_id]['balance']:.2f}")


def transfer(from_id, to_id, amount):
    if amount <= 0:
        print("Amount must be positive.")
        return
    accounts = load(ACCOUNTS_FILE)
    for aid in (from_id, to_id):
        if aid not in accounts:
            print(f"Account '{aid}' not found.")
            return
        if accounts[aid]["status"] == "closed":
            print(f"Account '{aid}' is closed.")
            return
    if accounts[from_id]["balance"] < amount:
        print(f"Insufficient balance. Available: {accounts[from_id]['balance']:.2f}")
        return
    accounts[from_id]["balance"] -= amount
    accounts[to_id]["balance"] += amount
    save(ACCOUNTS_FILE, accounts)
    _log_txn(from_id, "transfer_out", amount, accounts[from_id]["balance"], f"to {to_id}")
    _log_txn(to_id, "transfer_in", amount, accounts[to_id]["balance"], f"from {from_id}")
    logging.info(f"Transfer {amount} from {from_id} to {to_id}")
    print(f"Transferred {amount:.2f} from {from_id} to {to_id}.")


def mini_statement(acc_id):
    if not _check_active(acc_id):
        return
    records = load(TRANSACTIONS_FILE)
    if not isinstance(records, list):
        records = []
    txns = [r for r in records if r["account_id"] == acc_id][-5:]
    if not txns:
        print("No transactions yet.")
        return
    print(f"\n--- Mini Statement ({acc_id}) ---")
    print(f"{'Date':<22} {'Type':<15} {'Amount':>10} {'Balance':>10}")
    print("-" * 60)
    for t in txns:
        print(f"{t['date']:<22} {t['type']:<15} {t['amount']:>10.2f} {t['balance_after']:>10.2f}")


def transaction_history(acc_id):
    if not _check_active(acc_id):
        return
    records = load(TRANSACTIONS_FILE)
    if not isinstance(records, list):
        records = []
    txns = [r for r in records if r["account_id"] == acc_id]
    if not txns:
        print("No transactions yet.")
        return
    print(f"\n{'='*65}")
    print(f"  Transaction History — Account {acc_id}")
    print(f"{'='*65}")
    print(f"{'#':<5} {'Date':<22} {'Type':<15} {'Amount':>10} {'Balance':>10}")
    print(f"{'-'*65}")
    for t in txns:
        print(f"{t['id']:<5} {t['date']:<22} {t['type']:<15} {t['amount']:>10.2f} {t['balance_after']:>10.2f}")
    print(f"{'='*65}")
