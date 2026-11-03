"""
BranchCoverageTest_warranty_claims.py
Lab 6: Code and Branch Coverage Analysis
Author: Nagashri R Patil (PES1UG24CS289)

Target: warranty_claims.py
Objective: Deliverable adhering to BranchCoverageTest_xxxx_application.py.
Achieve 100% Branch Coverage across all decision branches, compound conditions,
and boundary values in warranty_claims.py.
"""

import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# =====================================================================
# Decision Branch Analysis for: out_of_warranty_charge
# =====================================================================

class TestOutOfWarrantyChargeBranchCoverage:
    """Complete branch coverage suite for out_of_warranty_charge."""

    def test_branch_plan_not_in_covered_months(self):
        """Branch: plan not in COVERED_MONTHS -> True (raises ValueError)."""
        with pytest.raises(ValueError, match="unknown plan"):
            out_of_warranty_charge("enterprise_vip", 12, "defect", False)

    def test_branch_plan_empty_string(self):
        """Branch: plan empty string not in COVERED_MONTHS -> True (raises ValueError)."""
        with pytest.raises(ValueError, match="unknown plan"):
            out_of_warranty_charge("", 10, "defect", False)

    def test_branch_negative_age_months(self):
        """Branch: age_months < 0 -> True (raises ValueError)."""
        with pytest.raises(ValueError, match="invalid age"):
            out_of_warranty_charge("basic", -1, "defect", False)

    def test_branch_negative_age_large(self):
        """Branch: age_months deeply negative -> True (raises ValueError)."""
        with pytest.raises(ValueError, match="invalid age"):
            out_of_warranty_charge("standard", -100, "accidental", True)

    def test_branch_registered_and_non_premium_basic(self):
        """
        Compound condition: is_registered=True AND plan != 'premium' -> True & True.
        Plan 'basic' (12 mo), registered (+6 mo) -> covered = 18.
        age = 23 -> excess = 5. Defect rate = 100 -> charge = 500.
        """
        assert out_of_warranty_charge("basic", 23, "defect", True) == 500

    def test_branch_registered_and_non_premium_standard(self):
        """
        Compound condition: is_registered=True AND plan != 'premium' -> True & True.
        Plan 'standard' (24 mo), registered (+6 mo) -> covered = 30.
        age = 35 -> excess = 5. Accidental rate = 200 -> charge = 1000.
        """
        assert out_of_warranty_charge("standard", 35, "accidental", True) == 1000

    def test_branch_registered_and_premium_plan(self):
        """
        Compound condition: is_registered=True AND plan == 'premium' -> True & False.
        Registered bonus NOT added for premium. Covered remains 36.
        age = 40 -> excess = 4. Defect rate = 100 -> charge = 400.
        """
        assert out_of_warranty_charge("premium", 40, "defect", True) == 400

    def test_branch_not_registered_basic(self):
        """
        Compound condition: is_registered=False AND plan != 'premium' -> False & True.
        Covered remains 12. age = 16 -> excess = 4. Defect rate = 100 -> charge = 400.
        """
        assert out_of_warranty_charge("basic", 16, "defect", False) == 400

    def test_branch_not_registered_premium(self):
        """
        Compound condition: is_registered=False AND plan == 'premium' -> False & False.
        Covered remains 36. age = 42 -> excess = 6. Accidental rate = 200 -> charge = 1200.
        """
        assert out_of_warranty_charge("premium", 42, "accidental", False) == 1200

    def test_branch_excess_zero_boundary(self):
        """Branch: excess <= 0 -> True (exact boundary: excess == 0)."""
        # basic = 12 months, unregistered, age = 12 -> excess = 0 -> returns 0
        assert out_of_warranty_charge("basic", 12, "defect", False) == 0

    def test_branch_excess_strictly_negative(self):
        """Branch: excess <= 0 -> True (excess < 0)."""
        # standard = 24 months, unregistered, age = 10 -> excess = -14 -> returns 0
        assert out_of_warranty_charge("standard", 10, "accidental", False) == 0

    def test_branch_excess_positive_accidental_moderate(self):
        """
        Branch: excess > 0, claim_type == 'accidental' -> True.
        excess <= 12 -> rate remains 200.
        basic = 12 mo, age = 20 -> excess = 8. charge = 8 * 200 = 1600.
        """
        assert out_of_warranty_charge("basic", 20, "accidental", False) == 1600

    def test_branch_excess_positive_defect_moderate(self):
        """
        Branch: excess > 0, claim_type != 'accidental' -> False (rate = 100).
        excess <= 12 -> rate remains 100.
        basic = 12 mo, age = 20 -> excess = 8. charge = 8 * 100 = 800.
        """
        assert out_of_warranty_charge("basic", 20, "defect", False) == 800

    def test_branch_excess_boundary_exact_twelve(self):
        """
        Branch: excess > 12 -> False (boundary condition excess == 12).
        basic = 12, unregistered, age = 24 -> excess = 12.
        claim_type = 'defect' -> rate remains 100. charge = 12 * 100 = 1200.
        """
        assert out_of_warranty_charge("basic", 24, "defect", False) == 1200

    def test_branch_excess_boundary_exact_twelve_accidental(self):
        """
        Branch: excess > 12 -> False (boundary condition excess == 12 for accidental).
        basic = 12, unregistered, age = 24 -> excess = 12.
        claim_type = 'accidental' -> rate remains 200. charge = 12 * 200 = 2400.
        """
        assert out_of_warranty_charge("basic", 24, "accidental", False) == 2400

    def test_branch_excess_greater_than_twelve_defect(self):
        """
        Branch: excess > 12 -> True, AND claim_type == 'accidental' -> False.
        rate = 100 + 50 = 150.
        basic = 12, unregistered, age = 26 -> excess = 14 (> 12).
        charge = 14 * 150 = 2100.
        """
        assert out_of_warranty_charge("basic", 26, "defect", False) == 2100

    def test_branch_excess_greater_than_twelve_accidental(self):
        """
        Branch: excess > 12 -> True, AND claim_type == 'accidental' -> True.
        rate = 200 + 50 + 25 = 275.
        basic = 12, unregistered, age = 26 -> excess = 14 (> 12).
        charge = 14 * 275 = 3850.
        """
        assert out_of_warranty_charge("basic", 26, "accidental", False) == 3850


# =====================================================================
# Decision Branch Analysis for: claim_allowed
# =====================================================================

class TestClaimAllowedBranchCoverage:
    """Complete branch coverage suite for claim_allowed."""

    def test_branch_recall_true_within_limit_boundary(self):
        """Branch: is_recall=True, claims_filed == 5 -> True."""
        assert claim_allowed(days_since_last_claim=5, claims_filed=5, is_recall=True) is True

    def test_branch_recall_true_zero_claims(self):
        """Branch: is_recall=True, claims_filed == 0 -> True."""
        assert claim_allowed(days_since_last_claim=0, claims_filed=0, is_recall=True) is True

    def test_branch_recall_true_exceeds_limit(self):
        """Branch: is_recall=True, claims_filed == 6 (> 5) -> False."""
        assert claim_allowed(days_since_last_claim=2, claims_filed=6, is_recall=True) is False

    def test_branch_non_recall_days_less_than_thirty(self):
        """Branch: is_recall=False, days_since_last_claim < 30 -> True (returns False)."""
        assert claim_allowed(days_since_last_claim=29, claims_filed=0, is_recall=False) is False

    def test_branch_non_recall_days_zero(self):
        """Branch: is_recall=False, days_since_last_claim == 0 -> returns False."""
        assert claim_allowed(days_since_last_claim=0, claims_filed=1, is_recall=False) is False

    def test_branch_non_recall_boundary_days_within_limit(self):
        """Branch: is_recall=False, days == 30 (>= 30), claims == 2 (<= 2) -> True."""
        assert claim_allowed(days_since_last_claim=30, claims_filed=2, is_recall=False) is True

    def test_branch_non_recall_boundary_days_zero_claims(self):
        """Branch: is_recall=False, days == 45, claims == 0 -> True."""
        assert claim_allowed(days_since_last_claim=45, claims_filed=0, is_recall=False) is True

    def test_branch_non_recall_days_sufficient_claims_exceeds_limit(self):
        """Branch: is_recall=False, days >= 30, claims == 3 (> 2) -> False."""
        assert claim_allowed(days_since_last_claim=30, claims_filed=3, is_recall=False) is False


# =====================================================================
# Decision Branch Analysis for: sla_status
# =====================================================================

class TestSlaStatusBranchCoverage:
    """Complete branch coverage suite for sla_status."""

    # --- Scenario 1: Non-hardware, Non-priority (cutoff = 24) ---
    def test_branch_sla_software_normal_on_track_boundary(self):
        """cutoff = 24. hours_left = 24 (>= cutoff) -> 'on_track'."""
        assert sla_status(24, is_hardware=False, is_priority=False) == "on_track"

    def test_branch_sla_software_normal_on_track_above(self):
        """cutoff = 24. hours_left = 30 (> cutoff) -> 'on_track'."""
        assert sla_status(30, is_hardware=False, is_priority=False) == "on_track"

    def test_branch_sla_software_normal_at_risk_upper(self):
        """cutoff = 24. hours_left = 23 (>= 12) -> 'at_risk'."""
        assert sla_status(23, is_hardware=False, is_priority=False) == "at_risk"

    def test_branch_sla_software_normal_at_risk_lower_boundary(self):
        """cutoff = 24. hours_left = 12 (exact cutoff - 12) -> 'at_risk'."""
        assert sla_status(12, is_hardware=False, is_priority=False) == "at_risk"

    def test_branch_sla_software_normal_critical_boundary(self):
        """cutoff = 24. hours_left = 11 (< 12) -> 'critical'."""
        assert sla_status(11, is_hardware=False, is_priority=False) == "critical"

    def test_branch_sla_software_normal_critical_zero(self):
        """cutoff = 24. hours_left = 0 -> 'critical'."""
        assert sla_status(0, is_hardware=False, is_priority=False) == "critical"

    # --- Scenario 2: Hardware, Non-priority (cutoff = 48) ---
    def test_branch_sla_hardware_normal_on_track(self):
        """cutoff = 48. hours_left = 48 -> 'on_track'."""
        assert sla_status(48, is_hardware=True, is_priority=False) == "on_track"

    def test_branch_sla_hardware_normal_at_risk(self):
        """cutoff = 48. cutoff - 12 = 36. hours_left = 36 -> 'at_risk'."""
        assert sla_status(36, is_hardware=True, is_priority=False) == "at_risk"

    def test_branch_sla_hardware_normal_critical(self):
        """cutoff = 48. hours_left = 35 -> 'critical'."""
        assert sla_status(35, is_hardware=True, is_priority=False) == "critical"

    # --- Scenario 3: Non-hardware, Priority (cutoff = 24 + 24 = 48) ---
    def test_branch_sla_software_priority_on_track(self):
        """cutoff = 48. hours_left = 50 -> 'on_track'."""
        assert sla_status(50, is_hardware=False, is_priority=True) == "on_track"

    def test_branch_sla_software_priority_at_risk(self):
        """cutoff = 48. hours_left = 40 (>= 36) -> 'at_risk'."""
        assert sla_status(40, is_hardware=False, is_priority=True) == "at_risk"

    def test_branch_sla_software_priority_critical(self):
        """cutoff = 48. hours_left = 30 (< 36) -> 'critical'."""
        assert sla_status(30, is_hardware=False, is_priority=True) == "critical"

    # --- Scenario 4: Hardware, Priority (cutoff = 48 + 24 = 72) ---
    def test_branch_sla_hardware_priority_on_track_boundary(self):
        """cutoff = 72. hours_left = 72 -> 'on_track'."""
        assert sla_status(72, is_hardware=True, is_priority=True) == "on_track"

    def test_branch_sla_hardware_priority_at_risk_boundary(self):
        """cutoff = 72. cutoff - 12 = 60. hours_left = 60 -> 'at_risk'."""
        assert sla_status(60, is_hardware=True, is_priority=True) == "at_risk"

    def test_branch_sla_hardware_priority_critical_boundary(self):
        """cutoff = 72. hours_left = 59 (< 60) -> 'critical'."""
        assert sla_status(59, is_hardware=True, is_priority=True) == "critical"
