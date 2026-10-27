# Lab 5: Static Code Analysis — Hotel Booking System

**Course:** Software Engineering Laboratory (UE23CS252AA)  
**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Assigned Source Repository:** [SETAPESU26/L5_43_hotel_booking_system](https://github.com/SETAPESU26/L5_43_hotel_booking_system)  
**Primary Program:** `hotel_booking_system.py`  

---

## Overview

This laboratory assignment demonstrates the application of multi-layered static code analysis to identify and remediate code quality defects, security vulnerabilities, and style violations in a Python application. The target system is a hotel room reservation and inventory management module (`hotel_booking_system.py`).

Three industry-standard static analysis tools were employed:
1. **Pylint (v4.1.3):** Evaluates code quality, conventions, potential runtime bugs, and architectural design patterns.
2. **Bandit (v1.9.4):** Performs AST-based application security audits to detect common vulnerabilities and security antipatterns (CWEs).
3. **Flake8 (v7.4.1):** Enforces PEP 8 style conformance, detects syntax errors, and flags unused symbols.

---

## Deliverables in This Directory

| File | Description |
|---|---|
| [`hotel_booking_system.py`](./hotel_booking_system.py) | Cleaned, secured, and PEP 8 compliant source code (Pylint: **10.00/10**, Bandit: **0 issues**, Flake8: **0 violations**). |
| [`test_hotel_booking.py`](./test_hotel_booking.py) | Unit test suite verifying functionality, edge cases, state isolation, and security controls (13/13 passing). |
| [`findings.md`](./findings.md) | Comprehensive table documenting all identified issues, line numbers, severity, fixes, and verification evidence. |
| [`reflection.md`](./reflection.md) | Detailed student-level answers to the five laboratory reflection questions. |
| [`pylint_report_before.txt`](./pylint_report_before.txt) | Baseline Pylint static analysis report before modifications (Score: **5.32/10**). |
| [`pylint_report_after.txt`](./pylint_report_after.txt) | Post-fix Pylint verification report demonstrating score of **10.00/10**. |
| [`bandit_report_before.txt`](./bandit_report_before.txt) | Baseline Bandit security scan report documenting 6 vulnerabilities (2 High, 1 Medium, 3 Low). |
| [`bandit_report_after.txt`](./bandit_report_after.txt) | Post-fix Bandit verification report showing **0 issues identified**. |
| [`flake8_report_before.txt`](./flake8_report_before.txt) | Baseline Flake8 style report listing 7 PEP 8 and lint violations. |
| [`flake8_report_after.txt`](./flake8_report_after.txt) | Post-fix Flake8 verification report confirming **0 style violations** (clean output). |

---

## Baseline vs. Post-Fix Comparison Summary

| Metric / Tool | Baseline (Before Fix) | Final (After Fix) | Outcome |
|---|---|---|---|
| **Pylint Rating** | `5.32 / 10` | **`10.00 / 10`** | **+4.68 improvement (Perfect score)** |
| **Bandit Findings** | 6 issues (2 High, 1 Med, 3 Low) | **0 issues** | **100% vulnerabilities resolved without suppression** |
| **Flake8 Violations** | 7 violations | **0 violations** | **Full PEP 8 compliance** |
| **Unit Tests Passing** | N/A (untested) | **13 / 13 passed** | **Core functionality & security controls verified** |

---

## Environment Setup & Reproduction Instructions

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.11.9)
- Git

### 2. Create and Activate Virtual Environment in Windows PowerShell

Create the virtual environment:
```powershell
python -m venv venv
```

Activate the virtual environment in Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

*(Optional) If script execution is restricted in PowerShell:*
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

*(Alternative for Windows Command Prompt):*
```cmd
.\venv\Scripts\activate.bat
```

### 3. Install Static Analysis Tools

Install Pylint, Bandit, and Flake8:
```powershell
pip install pylint bandit flake8
```

### 4. Run the Program

Execute the cleaned application:
```powershell
python hotel_booking_system.py
```

**Safe Expected Terminal Output (Default / Unconfigured):**
```text
Is 103 available: True
Surge price: 187.5
Guest Hash: 6d7f221fa359b1754599b3aa07ca54f52b4e136267d3e3b505fc5d64df61100d
Booking Reference: 7615
Hotel ledger exported to: hotel_ledger.txt
Secret key active: No (unconfigured)
```

*(Optional) Configure token via environment variable without hardcoding:*
```powershell
$env:HOTEL_ADMIN_RESERVATION_TOKEN = "MY_ADMIN_TOKEN_123"
python hotel_booking_system.py
```
Output confirms configuration safely without leaking secret values:
```text
Secret key active: Yes (configured via environment)
```

### 5. Run the Automated Unit Tests

Execute the unit test suite:
```powershell
python -m unittest test_hotel_booking.py
```

**Actual Verified Output:**
```text
.............
----------------------------------------------------------------------
Ran 13 tests in 0.011s

OK
```

### 6. Reproduce Static Code Analysis Reports

Run Pylint and save report:
```powershell
pylint hotel_booking_system.py > pylint_report_after.txt
```

Run Bandit and save report:
```powershell
bandit -r hotel_booking_system.py > bandit_report_after.txt
```

Run Flake8 and save report:
```powershell
flake8 hotel_booking_system.py > flake8_report_after.txt
```
