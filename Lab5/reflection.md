# Lab 5: Reflection on Static Code Analysis

**Course:** Software Engineering Laboratory (UE23CS252AA)  
**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Assigned Source Repository:** [SETAPESU26/L5_43_hotel_booking_system](https://github.com/SETAPESU26/L5_43_hotel_booking_system)  
**Program:** Hotel Room Reservation & Inventory Management (`hotel_booking_system.py`)  

---

## 1. What Static Code Analysis Is and Why It Is Useful

Static code analysis is the process of examining software source code without executing the program. By parsing the source code into an Abstract Syntax Tree (AST) and analyzing tokens, symbol tables, control flows, and structural patterns, static analysis tools detect coding errors, design antipatterns, security vulnerabilities, dead code, and style inconsistencies before runtime.

In software engineering, static code analysis is indispensable for several reasons:
- **Early Bug Detection:** It identifies subtle bugs (such as mutable default arguments, resource leaks, or missing return branches) during early development, long before software reaches integration or production testing.
- **Cost Reduction:** Fixing a defect identified during code composition or pre-commit checks is significantly faster and less expensive than diagnosing runtime failures or handling security breaches in production.
- **Security Hardening:** Specialized scanners automatically highlight vulnerable coding idioms—such as injection vectors, hardcoded secrets, and weak cryptography—ensuring applications adhere to secure coding standards (e.g., OWASP, CWE).
- **Automated Quality Governance:** It removes subjective human friction from peer reviews by enforcing standard coding conventions (such as PEP 8) and clean architecture guidelines consistently across distributed teams.

---

## 2. Differences Between Pylint, Bandit, and Flake8

Although all three tools analyze Python source code statically, they serve distinct and complementary purposes:

| Feature / Aspect | **Pylint** | **Bandit** | **Flake8** |
|---|---|---|---|
| **Primary Focus** | Code quality, architecture, potential bugs, docstrings, and comprehensive coding standards. | Application security, vulnerability scanning, and Common Weakness Enumeration (CWE) detection. | PEP 8 style conformance, syntax errors, and simple logical inconsistencies. |
| **Analysis Depth** | Deep semantic and AST analysis; tracks symbol definitions, type hints, variable lifetimes, and complexity metrics. | AST inspection targeting security-sensitive function calls, imports, string constants, and dangerous idioms. | Fast AST linting (via `pyflakes`), style auditing (via `pycodestyle`), and McCabe cyclomatic complexity. |
| **Scoring / Output** | Produces a quantitative quality rating out of 10.00 and detailed categorization (Convention, Refactor, Warning, Error). | Categorizes issues strictly by Severity (High, Medium, Low) and Confidence (High, Medium, Low) with CWE references. | Reports specific error/warning codes (e.g., E501 for line length, F401 for unused import) without a numeric score. |
| **Typical Use Case** | Comprehensive code review, refactoring assistance, and enforcing organizational best practices. | Security audits, DevSecOps CI/CD pipelines, and identifying penetration risks. | Rapid pre-commit git hooks, lightning-fast developer feedback, and stylistic uniformity. |

---

## 3. The Most Important Issues Found in This Program

Analyzing `hotel_booking_system.py` revealed several critical vulnerabilities and defects:

1. **Arbitrary Dynamic Code Execution (`eval`) — Severity: Medium (Bandit B307, Pylint W0123):**  
   In `compute_seasonal_rate()`, the program called `eval(rate_expr)`. Passing dynamically constructed or user-controllable mathematical expressions directly to `eval()` allows an attacker to break out of mathematical context and execute arbitrary Python expressions or OS commands (e.g., `__import__('os').system('rm -rf /')`), leading to total host compromise.
2. **Command Injection Vulnerability (`os.system`) — Severity: High (Bandit B605):**  
   In `export_room_ledger()`, the script spawned an OS shell using `os.system("echo Hotel ledger exported to: " + filename)`. If `filename` contained shell metacharacters (e.g., `;`, `&`, `|`), external shell commands would execute under the permissions of the application process.
3. **Dangerous Mutable Default Argument (`booking_log=[]`) — Severity: Medium (Pylint W0102):**  
   In Python, default arguments are instantiated once when the function is defined, not on each invocation. As a result, subsequent calls to `book_room()` without an explicit list appended records to the same shared list, leaking private reservation logs between different guests.
4. **Weak Cryptography and Hardcoded Secrets (Bandit B324, B311, B105):**  
   The program utilized MD5 (which is vulnerable to collisions) for guest identity hashing, standard Mersenne Twister pseudo-random numbers (`random.randint`) for reservation references, and an administrative secret token embedded directly in source text.
5. **Bare Exception Handling (`except: pass`) — Flake8 E722, Pylint W0702, Bandit B110:**  
   `cancel_booking()` caught all exceptions indiscriminately and suppressed them with `pass`. This swallowed unexpected critical failures (such as `KeyboardInterrupt`, memory errors, or unrelated bugs) silently.

---

## 4. How the Fixes Improved Code Quality, Security, and Maintainability

Applying targeted fixes directly addressed all identified flaws:

- **Security Hardening:**
  - Replacing `eval()` with an AST-based arithmetic parser (`_safe_eval_math()`) restricted evaluation exclusively to verified binary operations (`+`, `-`, `*`, `/`) on numeric constants and `base_price`, eliminating remote code execution risks while preserving formula flexibility.
  - Eliminating `os.system()` in favor of native Python `print()` permanently prevented shell injection attacks and removed platform-dependent shell dependencies.
  - Upgrading to `hashlib.sha256` ensured collision-resistant cryptographic hashing.
  - Switching to `secrets.SystemRandom().randint(1000, 9999)` provided cryptographically secure randomness suitable for reservation references.
  - Sourcing credentials from environment variables (`os.environ.get`) kept secrets out of version control.
- **Correctness and Reliability:**
  - Replacing mutable default argument `booking_log=[]` with `booking_log=None` ensured state isolation across independent booking transactions.
  - Replacing bare `except:` with explicit dictionary membership verification (`if room_num in room_inventory:`) prevented silent masking of critical system exceptions.
  - Utilizing `with open(..., encoding="utf-8")` ensured file handles are deterministically closed even in the event of I/O errors, preventing resource leaks.
- **Maintainability and Readability:**
  - Standardizing function names to `snake_case` (`book_room`) and adding informative docstrings clarifies module behavior for future developers.
  - Adhering strictly to PEP 8 formatting (line length <= 79 characters, consistent whitespace, removing dead code and unused imports) makes the codebase clean, professional, and easy to maintain.

---

## 5. What I Learned from Comparing the Before-and-After Reports

Comparing the baseline reports with the post-fix reports provided concrete quantitative insights:

1. **Measurable Quality Improvement:**  
   The quantitative metrics demonstrated a clear transformation:
   - **Pylint:** Rose from an initial **5.32 / 10** to a perfect **10.00 / 10**.
   - **Bandit:** Dropped from **6 issues** (2 High, 1 Medium, 3 Low) down to **0 issues** across all severity levels.
   - **Flake8:** Dropped from **7 violations** to **0 violations**.
2. **Complementary Power of Layered Static Tools:**  
   No single tool caught every flaw. Flake8 was essential for syntax formatting, bare except detection, and PEP 8 alignment; Pylint excels at structural design, docstring completeness, and variable lifetimes; while Bandit discovered subtle security hazards (such as MD5 hashing and shell command injection) that neither Flake8 nor Pylint prioritized. Employing a layered multi-tool analysis workflow is vital for robust engineering.
3. **Fixing Underlying Causes vs. Suppressing Warnings:**  
   Achieving high scores without `# noqa`, `#nosec`, or `# pylint: disable` annotations required addressing the underlying architectural and security flaws at their root. Writing safe AST parsers, adopting modern standard library modules (`secrets`, `hashlib.sha256`), and using Pythonic context managers resolved warnings naturally while simultaneously making the program safer, faster, and more robust.
