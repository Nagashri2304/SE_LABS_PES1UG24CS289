"""
warranty_claims.py (Hardened against Fuzz Testing / Malformed Inputs)
Lab 7: Fuzzing for Input Validation Bugs
Author: Nagashri R Patil (PES1UG24CS289)

Objective: Harden all input-handling functions against unexpected, malformed,
and edge-case inputs discovered through Hypothesis property-based fuzz testing.
"""

def parse_claim(text):
    """
    Safely parses plan and age in months from 'plan:months' string.
    Hardened against NoneType, delimiter absence/multiplicity, and non-numeric values.
    Returns: (plan_title, months_float) or (None, 0.0) on invalid input.
    """
    if not isinstance(text, str):
        return None, 0.0
    if ':' not in text:
        return None, 0.0
    parts = text.split(':')
    if len(parts) != 2:
        return None, 0.0
    plan = parts[0].strip().title()
    try:
        months = float(parts[1].strip())
        return (plan if plan else "Unknown"), months
    except (ValueError, TypeError):
        return None, 0.0


def age_average(ages_csv):
    """
    Safely calculates integer average of product ages from a CSV string.
    Hardened against NoneType, empty inputs, non-integer tokens, and ZeroDivisionError.
    Returns: integer average or 0 on empty/invalid input.
    """
    if not isinstance(ages_csv, str):
        return 0
    clean = ages_csv.strip()
    if not clean:
        return 0
    parts = clean.split(',')
    values = []
    for r in parts:
        token = r.strip()
        if token:
            try:
                values.append(int(token))
            except (ValueError, TypeError):
                continue
    if not values:
        return 0
    return sum(values) // len(values)


def payable_charge(text):
    """
    Safely computes payable charge after discount from 'charge|discount' string.
    Formula: max(charge * 1.18 - discount, 0)
    Hardened against NoneType, delimiter issues, and non-numeric values.
    Returns: payable charge float or 0.0 on invalid input.
    """
    if not isinstance(text, str):
        return 0.0
    if '|' not in text:
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    try:
        charge = float(parts[0].strip())
        discount = float(parts[1].strip())
        total = charge * 1.18 - discount
        return max(total, 0.0)
    except (ValueError, TypeError):
        return 0.0


def main():
    print("==== Running parse_claim ====")
    user_input = input("Enter plan:age in months (e.g. standard:30): ")
    result = parse_claim(user_input)
    print("Plan and Age:", result)

    print("\n==== Running age_average ====")
    user_input = input("Enter product ages as CSV (e.g. 12,24,36): ")
    result = age_average(user_input)
    print("Average Age:", result)

    print("\n==== Running payable_charge ====")
    user_input = input("Enter charge|discount (e.g. 1500|200): ")
    result = payable_charge(user_input)
    print("Payable Charge:", result)


if __name__ == "__main__":
    main()
