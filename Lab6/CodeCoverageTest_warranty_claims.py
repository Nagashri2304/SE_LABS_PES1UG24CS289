"""
CodeCoverageTest_warranty_claims.py
Lab 6: Code and Branch Coverage Analysis
Author: Nagashri R Patil (PES1UG24CS289)

Target: warranty_claims.py
Objective: Achieve >= 90% (100%) Statement / Line Code Coverage.
"""

import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# =====================================================================
# Initial Example Test Cases (from starter test suite)
# =====================================================================

def test_within_warranty_example():
    """Initial test: Within warranty coverage (excess <= 0)."""
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_claim_allowed_example():
    """Initial test: Claim allowed when days >= 30 and claims <= 2."""
    assert claim_allowed(60, 1, False) is True


# =====================================================================
# Targeted Test Cases for Line / Statement Coverage of warranty_claims.py
# =====================================================================

def test_out_of_warranty_unknown_plan_raises_error():
    """Executes lines 5-6: ValueError on unregistered plan name."""
    with pytest.raises(ValueError, match="unknown plan"):
        out_of_warranty_charge("enterprise", 12, "defect", False)


def test_out_of_warranty_invalid_negative_age_raises_error():
    """Executes lines 7-8: ValueError on negative age_months."""
    with pytest.raises(ValueError, match="invalid age"):
        out_of_warranty_charge("basic", -5, "defect", False)


def test_out_of_warranty_registered_basic_defect_moderate_excess():
    """
    Executes lines 9-14, 17-18, 23:
    Plan 'basic' (12 mo), registered (+6 mo) -> covered = 18.
    age = 22 -> excess = 4 (<= 12).
    claim_type = 'defect' -> rate = 100.
    charge = 4 * 100 = 400.
    """
    assert out_of_warranty_charge("basic", 22, "defect", True) == 400


def test_out_of_warranty_registered_standard_accidental_large_excess():
    """
    Executes lines 10-11, 15-16, 19-22, 23:
    Plan 'standard' (24 mo), registered (+6 mo) -> covered = 30.
    age = 45 -> excess = 15 (> 12).
    claim_type = 'accidental' -> base rate 200 + 50 + 25 = 275.
    charge = 15 * 275 = 4125.
    """
    assert out_of_warranty_charge("standard", 45, "accidental", True) == 4125


def test_out_of_warranty_excess_large_non_accidental():
    """
    Executes lines 19-20 (excess > 12 with non-accidental claim).
    Plan 'basic' (12 mo), unregistered -> covered = 12.
    age = 28 -> excess = 16 (> 12).
    claim_type = 'defect' -> rate = 100 + 50 = 150.
    charge = 16 * 150 = 2400.
    """
    assert out_of_warranty_charge("basic", 28, "defect", False) == 2400


def test_claim_allowed_recall_valid():
    """Executes lines 27-28: is_recall=True with claims_filed <= 5."""
    assert claim_allowed(days_since_last_claim=10, claims_filed=3, is_recall=True) is True


def test_claim_allowed_recall_rejected():
    """Executes line 28 (False outcome): is_recall=True with claims_filed > 5."""
    assert claim_allowed(days_since_last_claim=10, claims_filed=6, is_recall=True) is False


def test_claim_allowed_recent_claim_rejected():
    """Executes lines 29-30: not recall, days_since_last_claim < 30 returns False."""
    assert claim_allowed(days_since_last_claim=15, claims_filed=0, is_recall=False) is False


def test_claim_allowed_exceeds_normal_limit_rejected():
    """Executes line 31 (False outcome): days >= 30 but claims_filed > 2."""
    assert claim_allowed(days_since_last_claim=45, claims_filed=3, is_recall=False) is False


def test_sla_status_hardware_priority_on_track():
    """
    Executes lines 35-36, 39-40, 41-42:
    is_hardware=True (cutoff=48), is_priority=True (cutoff=72).
    hours_left = 75 >= 72 -> returns 'on_track'.
    """
    assert sla_status(hours_left=75, is_hardware=True, is_priority=True) == "on_track"


def test_sla_status_software_non_priority_at_risk():
    """
    Executes lines 37-38, 43-44:
    is_hardware=False (cutoff=24), is_priority=False.
    hours_left = 18 >= 12 -> returns 'at_risk'.
    """
    assert sla_status(hours_left=18, is_hardware=False, is_priority=False) == "at_risk"


def test_sla_status_software_non_priority_critical():
    """
    Executes line 45:
    is_hardware=False (cutoff=24), is_priority=False.
    hours_left = 5 < 12 -> returns 'critical'.
    """
    assert sla_status(hours_left=5, is_hardware=False, is_priority=False) == "critical"
