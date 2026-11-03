import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ── membership_cost tests ──

def test_monthly_plan_basic():
    """Basic monthly plan, no discounts, no trainer."""
    assert membership_cost("monthly", 30, False, False) == 1500


def test_quarterly_plan_basic():
    """Basic quarterly plan, no discounts, no trainer."""
    assert membership_cost("quarterly", 30, False, False) == 4000


def test_yearly_plan_basic():
    """Basic yearly plan, no discounts, no trainer."""
    assert membership_cost("yearly", 30, False, False) == 12000


def test_senior_discount():
    """Senior (age >= 60) gets 25% discount."""
    # 1500 - 1500//4 = 1500 - 375 = 1125
    assert membership_cost("monthly", 65, False, False) == 1125


def test_student_discount():
    """Student gets 10% discount (non-senior)."""
    # 1500 - 1500//10 = 1500 - 150 = 1350
    assert membership_cost("monthly", 20, True, False) == 1350


def test_senior_overrides_student():
    """Senior discount applies even if is_student is True."""
    # Senior takes priority (elif), so 25% discount
    assert membership_cost("monthly", 60, True, False) == 1125


def test_with_trainer_monthly():
    """Trainer adds 2000 for non-yearly plan."""
    assert membership_cost("monthly", 30, False, True) == 1500 + 2000


def test_with_trainer_yearly():
    """Trainer adds 2000 but yearly gets 500 discount on trainer."""
    assert membership_cost("yearly", 30, False, True) == 12000 + 2000 - 500


def test_unknown_plan():
    """Unknown plan raises ValueError."""
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 30, False, False)


def test_too_young():
    """Age < 14 raises ValueError."""
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)


# ── can_enter tests ──

def test_can_enter_normal():
    """Active plan, normal hours, not women-only."""
    assert can_enter(10, True, False, "M") is True


def test_cannot_enter_inactive_plan():
    """Inactive plan cannot enter."""
    assert can_enter(10, False, False, "M") is False


def test_cannot_enter_too_early():
    """Before 5 AM cannot enter."""
    assert can_enter(4, True, False, "M") is False


def test_cannot_enter_too_late():
    """After 22 (10 PM) cannot enter."""
    assert can_enter(23, True, False, "M") is False


def test_women_only_female():
    """Women-only slot, female can enter."""
    assert can_enter(10, True, True, "F") is True


def test_women_only_male():
    """Women-only slot, male cannot enter."""
    assert can_enter(10, True, True, "M") is False


# ── bmi_category tests ──

def test_bmi_underweight():
    """BMI < 18.5 → underweight."""
    assert bmi_category(50, 1.75) == "underweight"


def test_bmi_normal():
    """18.5 <= BMI < 25 → normal."""
    assert bmi_category(70, 1.75) == "normal"


def test_bmi_overweight():
    """25 <= BMI < 30 → overweight."""
    assert bmi_category(85, 1.75) == "overweight"


def test_bmi_obese():
    """BMI >= 30 → obese."""
    assert bmi_category(100, 1.75) == "obese"


def test_bmi_invalid_height():
    """Height <= 0 raises ValueError."""
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, 0)
