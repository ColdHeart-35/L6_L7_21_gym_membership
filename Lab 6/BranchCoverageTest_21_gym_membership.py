import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ══════════════════════════════════════════════════════════════
#  membership_cost — every branch True/False
# ══════════════════════════════════════════════════════════════

# Branch: plan not in PLAN_PRICE → True
def test_invalid_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 30, False, False)


# Branch: plan not in PLAN_PRICE → False (valid plans)
def test_monthly_plan():
    assert membership_cost("monthly", 30, False, False) == 1500


def test_quarterly_plan():
    assert membership_cost("quarterly", 30, False, False) == 4000


def test_yearly_plan():
    assert membership_cost("yearly", 30, False, False) == 12000


# Branch: age < 14 → True
def test_too_young():
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)


# Branch: age < 14 → False
def test_age_exactly_14():
    assert membership_cost("monthly", 14, False, False) == 1500


# Branch: age >= 60 → True
def test_senior_discount():
    # 1500 - 1500//4 = 1125
    assert membership_cost("monthly", 60, False, False) == 1125


# Branch: age >= 60 → False, is_student → True
def test_student_discount():
    # 1500 - 1500//10 = 1350
    assert membership_cost("monthly", 20, True, False) == 1350


# Branch: age >= 60 → False, is_student → False (no discount)
def test_no_discount():
    assert membership_cost("monthly", 30, False, False) == 1500


# Branch: with_trainer → True, plan == "yearly" → True
def test_trainer_yearly():
    # 12000 + 2000 - 500 = 13500
    assert membership_cost("yearly", 30, False, True) == 13500


# Branch: with_trainer → True, plan == "yearly" → False
def test_trainer_non_yearly():
    assert membership_cost("monthly", 30, False, True) == 3500


# Branch: with_trainer → False
def test_no_trainer():
    assert membership_cost("monthly", 30, False, False) == 1500


# ══════════════════════════════════════════════════════════════
#  can_enter — every branch True/False
# ══════════════════════════════════════════════════════════════

# Branch: not plan_active → True
def test_inactive_plan():
    assert can_enter(10, False, False, "M") is False


# Branch: not plan_active → False (active)
def test_active_plan():
    assert can_enter(10, True, False, "M") is True


# Branch: hour < 5 → True
def test_too_early():
    assert can_enter(4, True, False, "M") is False


# Branch: hour > 22 → True
def test_too_late():
    assert can_enter(23, True, False, "M") is False


# Branch: hour < 5 → False AND hour > 22 → False (within range)
def test_valid_hour():
    assert can_enter(10, True, False, "M") is True


# Boundary: hour == 5 (allowed)
def test_hour_boundary_5():
    assert can_enter(5, True, False, "M") is True


# Boundary: hour == 22 (allowed)
def test_hour_boundary_22():
    assert can_enter(22, True, False, "M") is True


# Branch: is_women_only_slot → True, gender == "F" → True
def test_women_only_female():
    assert can_enter(10, True, True, "F") is True


# Branch: is_women_only_slot → True, gender == "F" → False
def test_women_only_male():
    assert can_enter(10, True, True, "M") is False


# Branch: is_women_only_slot → False
def test_not_women_only():
    assert can_enter(10, True, False, "M") is True


# ══════════════════════════════════════════════════════════════
#  bmi_category — every branch True/False
# ══════════════════════════════════════════════════════════════

# Branch: height_m <= 0 → True
def test_invalid_height_zero():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, 0)


def test_invalid_height_negative():
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, -1)


# Branch: height_m <= 0 → False (valid height)
# Branch: bmi < 18.5 → True
def test_underweight():
    assert bmi_category(50, 1.75) == "underweight"


# Branch: bmi < 18.5 → False, bmi < 25 → True
def test_normal():
    assert bmi_category(70, 1.75) == "normal"


# Branch: bmi < 25 → False, bmi < 30 → True
def test_overweight():
    assert bmi_category(85, 1.75) == "overweight"


# Branch: bmi < 30 → False (obese)
def test_obese():
    assert bmi_category(100, 1.75) == "obese"


# Boundary: BMI exactly 18.5 → normal
def test_bmi_boundary_18_5():
    # weight / (height^2) = 18.5  →  weight = 18.5 * 1.0^2 = 18.5
    assert bmi_category(18.5, 1.0) == "normal"


# Boundary: BMI exactly 25 → overweight
def test_bmi_boundary_25():
    assert bmi_category(25, 1.0) == "overweight"


# Boundary: BMI exactly 30 → obese
def test_bmi_boundary_30():
    assert bmi_category(30, 1.0) == "obese"
