# Day 12 — Banking Management System

**Internship Task | Python | June 27, 2026**

---

## Topic

Banking Management System — a modular, console-based Python project with authentication, banking operations, account management, and reporting with persistent JSON storage.

---

## Task Requirements

- Develop a modular Banking Management System (Console Application)
- **Authentication:** Login, Register, Change Password
- **Banking:** Deposit, Withdraw, Transfer Money, Mini Statement, Transaction History
- **Account Management:** Create Account, Close Account, Update Details
- **Reports:** Daily Transactions, Monthly Report, Customer Summary
- Requirements: Functions, Modules, File Handling, Exception Handling, JSON Storage, Logging
- **Bonus:** Encrypt passwords before saving (SHA-256)

---

## Deliverables

| Deliverable | Status | Details |
|---|---|---|
| ✅ Python Project Structure | Complete | 6-module structure: `storage` → `auth`/`accounts`/`banking`/`reports` → `main` |
| ✅ GitHub Repository | Complete | [day-12 branch](https://github.com/Prajjwal-Jyotishi/instadot-internship-prajjwal-jyotishi/tree/day-12) |
| ✅ Clean Source Code | Complete | Minimal, readable, modular |
| ✅ Console Output Screenshots | Complete | 6 screenshots in `screenshots/` folder |
| ✅ Bonus: Password Encryption | Complete | SHA-256 hashing via `hashlib` |

---

## Project Structure

```
banking_system/
├── main.py          # Entry point — two-phase CLI menu (auth + banking)
├── storage.py       # File I/O layer (JSON persistence + logging setup)
├── auth.py          # Authentication — register, login, change password (SHA-256)
├── accounts.py      # Account management — create, close, update details
├── banking.py       # Banking ops — deposit, withdraw, transfer, statements
├── reports.py       # Reports — daily transactions, monthly report, customer summary
├── screenshots/     # Output screenshots
└── data/            # Auto-created at runtime
    ├── users.json         # User credentials (encrypted passwords)
    ├── accounts.json      # Account details
    ├── transactions.json  # All transaction records
    └── banking.log        # Application log
```

---

## How to Run

```bash
python banking_system/main.py
```

---

## Output Screenshots

### 1. Register & Login
![Register and Login](banking_system/screenshots/output_1_register_login.png)

### 2. Create Account & Deposit
![Create Account and Deposit](banking_system/screenshots/output_2_create_deposit.png)

### 3. Withdraw & Transfer
![Withdraw and Transfer](banking_system/screenshots/output_3_withdraw_transfer.png)

### 4. Mini Statement & Transaction History
![Statements](banking_system/screenshots/output_4_statement_history.png)

### 5. Daily Transactions, Monthly Report & Customer Summary
![Reports](banking_system/screenshots/output_5_reports.png)

### 6. Update Details, Close Account & Change Password
![Update Close Password](banking_system/screenshots/output_6_update_close.png)
