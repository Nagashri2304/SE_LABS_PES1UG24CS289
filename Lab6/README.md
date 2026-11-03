# Lab 6: Code and Branch Coverage Analysis

**Student Name:** Nagashri R Patil  
**SRN:** PES1UG24CS289  
**Course:** Software Engineering Laboratory (UE23CS252AA)  
**Institution:** PES University, Department of Computer Science & Engineering  
**Assigned Individual Repository:** [SETAPESU26/L6_L7_43_warranty_claims](https://github.com/SETAPESU26/L6_L7_43_warranty_claims)  
**Assigned Problem Statement:** #43 – Warranty Claims Processing System (`warranty_claims.py`)  

---

## 1. Objectives & Overview

The primary objectives of this laboratory exercise are:
1. Understand the core conceptual and practical differences between **Code (Line / Statement) Coverage** and **Branch Coverage**.
2. Measure, analyze, and systematically improve test coverage using Python's `coverage` library and `pytest` framework.
3. Interpret coverage reports, uncover untested execution paths, and identify hidden edge cases or dead code.
4. Design targeted, robust test suites achieving **>90% to 100%** code and branch coverage on the assigned business logic module (`warranty_claims.py`).

### Software Requirements
- **Python:** 3.11+
- **pytest:** 9.2.0 (`pip install pytest`)
- **coverage:** 7.17.1 (`pip install coverage`)

---

## 2. Module Under Test: `warranty_claims.py`

The module under test simulates an automated warranty claims processing engine consisting of three core functions:

1. `out_of_warranty_charge(plan, age_months, claim_type, is_registered)`:
   - Calculates repair and service charges for products out of warranty based on warranty plan tier (`basic` = 12 months, `standard` = 24 months, `premium` = 36 months).
   - Grants a 6-month coverage extension if the product is registered and on a non-premium plan.
   - Evaluates excess months and applies base and penalty rates:
     - Normal rate: $100/mo (defect) or $200/mo (accidental).
     - Aging surcharge for `excess > 12`: +$50/mo, plus an additional +$25/mo surcharge for accidental claims.
   - Raises `ValueError` for unknown plan names or negative product ages.

2. `claim_allowed(days_since_last_claim, claims_filed, is_recall)`:
   - Evaluates whether a customer is permitted to file a claim.
   - For recall claims (`is_recall=True`), permits filing if lifetime claims filed $\le 5$.
   - For standard claims, enforces a 30-day waiting period between claims (`days_since_last_claim >= 30`) and a maximum limit of 2 previous claims (`claims_filed <= 2`).

3. `sla_status(hours_left, is_hardware, is_priority)`:
   - Determines the Service Level Agreement (SLA) operational status: `"on_track"`, `"at_risk"`, or `"critical"`.
   - Computes baseline cutoffs: 48 hours for hardware, 24 hours for software.
   - Adds an additional 24 hours cutoff buffer for priority service requests.
   - Thresholds:
     - `hours_left >= cutoff`: `"on_track"`
     - `cutoff - 12 <= hours_left < cutoff`: `"at_risk"`
     - `hours_left < cutoff - 12`: `"critical"`

---

## 3. Baseline / Initial Test Coverage Analysis

### Initial Test Suite (`test_warranty_claims.py`)
The starter repository provided two basic test cases:
- `test_within_warranty`: Verifies standard plan with age 20 months returns 0.
- `test_claim_allowed`: Verifies claim filing allowed for 60 days and 1 claim.

### Initial Execution Command
```powershell
coverage run -m pytest test_warranty_claims.py
coverage report -m
```

### Initial Terminal Output Screenshot
![Initial Coverage Screenshot](./screenshots/01_initial_coverage.png)

### Initial Coverage Metrics Table
| Module | Statements | Missing Lines | Statement Coverage | Missing Line Numbers |
| :--- | :---: | :---: | :---: | :--- |
| `warranty_claims.py` | 37 | 23 | **38%** | 6, 8, 11, 15-23, 28, 30, 35-45 |
| `test_warranty_claims.py` | 6 | 0 | 100% | None |
| **Total** | **43** | **23** | **47%** | — |

### Identified Untested Paths & Deficiencies
1. **Error Handling Paths:** Neither invalid plan validation (lines 5-6) nor negative age validation (lines 7-8) was tested.
2. **Registration Bonus:** The 6-month extension logic for registered non-premium accounts was unexercised.
3. **Out-of-Warranty Pricing:** Accidental claim rates ($200), excess surcharge thresholds ($> 12$ months), and compound accidental surcharges were untested.
4. **Recall & Cooldown Rejections:** Boundary checks for `is_recall` limits and cooldown rejections (`days < 30`) were omitted.
5. **SLA Calculation:** The entire `sla_status` function (lines 35-45) was untouched (0% coverage).

---

## 4. Code Coverage (Statement / Line Coverage) Analysis

### Concept of Code Coverage
Code coverage measures the proportion of source code statements executed during test execution. A line is considered covered if the execution pointer traversed that statement at least once.

### Test Suite Design (`CodeCoverageTest_warranty_claims.py`)
To achieve $\ge 90\%$ code coverage, 14 targeted test cases were developed to traverse every executable statement:
1. `test_within_warranty_example`: Within warranty boundary check.
2. `test_claim_allowed_example`: Normal claim approval check.
3. `test_out_of_warranty_unknown_plan_raises_error`: Exercises `raise ValueError("unknown plan")`.
4. `test_out_of_warranty_invalid_negative_age_raises_error`: Exercises `raise ValueError("invalid age")`.
5. `test_out_of_warranty_registered_basic_defect_moderate_excess`: Exercises registered coverage addition and defect baseline charge.
6. `test_out_of_warranty_registered_standard_accidental_large_excess`: Exercises accidental rate and excess surcharge branches.
7. `test_out_of_warranty_excess_large_non_accidental`: Exercises non-accidental surcharge line.
8. `test_claim_allowed_recall_valid`: Exercises recall approval branch.
9. `test_claim_allowed_recall_rejected`: Exercises recall rejection limit.
10. `test_claim_allowed_recent_claim_rejected`: Exercises 30-day cooldown rejection.
11. `test_claim_allowed_exceeds_normal_limit_rejected`: Exercises standard claim quota rejection.
12. `test_sla_status_hardware_priority_on_track`: Exercises hardware + priority `"on_track"` execution path.
13. `test_sla_status_software_non_priority_at_risk`: Exercises software `"at_risk"` execution path.
14. `test_sla_status_software_non_priority_critical`: Exercises `"critical"` SLA status return.

### Code Coverage Execution Command
```powershell
coverage run -m pytest CodeCoverageTest_warranty_claims.py
coverage report -m
```

### Code Coverage Terminal Output Screenshot
![Code Coverage Analysis Screenshot](./screenshots/02_code_coverage_analysis.png)

### Code Coverage Report Table
| File | Statements | Missing Lines | Coverage | Status |
| :--- | :---: | :---: | :---: | :---: |
| `CodeCoverageTest_warranty_claims.py` | 32 | 0 | 100% | Passed (14/14) |
| `warranty_claims.py` | 37 | 0 | **100%** | **Target Achieved (>90%)** |
| **TOTAL** | **69** | **0** | **100%** | **Target Achieved (>90%)** |

---
*(Branch coverage analysis and complete comparative evaluation will be committed in the subsequent branch coverage milestone deliverable).*
