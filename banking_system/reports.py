from storage import load, ACCOUNTS_FILE, TRANSACTIONS_FILE


def daily_transactions(date_str):
    records = load(TRANSACTIONS_FILE)
    if not isinstance(records, list):
        records = []
    txns = [r for r in records if r["date"].startswith(date_str)]
    if not txns:
        print(f"No transactions on {date_str}.")
        return
    print(f"\n{'='*65}")
    print(f"  Daily Transactions — {date_str}")
    print(f"{'='*65}")
    print(f"{'#':<5} {'Account':<10} {'Type':<15} {'Amount':>10} {'Balance':>10}")
    print(f"{'-'*65}")
    for t in txns:
        print(f"{t['id']:<5} {t['account_id']:<10} {t['type']:<15} {t['amount']:>10.2f} {t['balance_after']:>10.2f}")
    print(f"{'='*65}")
    print(f"Total transactions: {len(txns)}")


def monthly_report(year, month):
    prefix = f"{year}-{month:02d}"
    records = load(TRANSACTIONS_FILE)
    if not isinstance(records, list):
        records = []
    txns = [r for r in records if r["date"].startswith(prefix)]
    if not txns:
        print(f"No transactions in {prefix}.")
        return
    total_in = sum(t["amount"] for t in txns if t["type"] in ("deposit", "transfer_in"))
    total_out = sum(t["amount"] for t in txns if t["type"] in ("withdraw", "transfer_out"))
    print(f"\n{'='*50}")
    print(f"  Monthly Report — {month:02d}/{year}")
    print(f"{'='*50}")
    print(f"  Total Transactions : {len(txns)}")
    print(f"  Total Credits      : {total_in:.2f}")
    print(f"  Total Debits       : {total_out:.2f}")
    print(f"  Net Flow           : {total_in - total_out:.2f}")
    print(f"{'='*50}")


def customer_summary(acc_id):
    accounts = load(ACCOUNTS_FILE)
    if acc_id not in accounts:
        print(f"Account '{acc_id}' not found.")
        return
    acc = accounts[acc_id]
    records = load(TRANSACTIONS_FILE)
    if not isinstance(records, list):
        records = []
    txns = [r for r in records if r["account_id"] == acc_id]
    print(f"\n{'='*45}")
    print(f"  Customer Summary — {acc_id}")
    print(f"{'='*45}")
    print(f"  Name    : {acc['name']}")
    print(f"  Type    : {acc['type']}")
    print(f"  Status  : {acc['status']}")
    print(f"  Balance : {acc['balance']:.2f}")
    print(f"  Created : {acc['created']}")
    print(f"  Total Txns : {len(txns)}")
    print(f"{'='*45}")
