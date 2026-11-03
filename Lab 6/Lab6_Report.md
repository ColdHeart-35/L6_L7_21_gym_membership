# Lab 6: Code and Branch Coverage Analysis — Report

## Objective

To understand the difference between code (line) coverage and branch coverage,
use the `coverage` tool to measure and improve test coverage, and write
comprehensive test cases that cover edge cases and decision branches for the
`gym_membership.py` application.

## Application Under Test

**File:** `gym_membership.py`

The module contains three functions:

| Function | Purpose |
|----------|---------|
| `membership_cost(plan, age, is_student, with_trainer)` | Calculates gym membership cost with discounts (senior 25%, student 10%) and optional trainer add-on (₹2000, with ₹500 yearly discount). |
| `can_enter(hour, plan_active, is_women_only_slot, gender)` | Checks if a member can enter the gym based on active plan, operating hours (5–22), and women-only slot rules. |
| `bmi_category(weight_kg, height_m)` | Returns BMI category: underweight, normal, overweight, or obese. |

## Code Coverage Analysis

**Test file:** `CodeCoverageTest_21_gym_membership.py`
**Tests written:** 21
**Tests passed:** 21

### Command Used

```
coverage run --source=. -m pytest CodeCoverageTest_21_gym_membership.py -v
coverage report -m --include=gym_membership.py
```

### Result

| File | Stmts | Miss | Cover |
|------|-------|------|-------|
| gym_membership.py | 35 | 0 | **100%** |

All 35 statements in the application are executed by the test cases.

## Branch Coverage Analysis

**Test file:** `BranchCoverageTest_21_gym_membership.py`
**Tests written:** 31
**Tests passed:** 31

### Command Used

```
coverage run --branch --source=. -m pytest BranchCoverageTest_21_gym_membership.py -v
coverage report -m --include=gym_membership.py
```

### Result

| File | Stmts | Miss | Branch | BrPart | Cover |
|------|-------|------|--------|--------|-------|
| gym_membership.py | 35 | 0 | 26 | 0 | **100%** |

All 26 branches are covered. Every `if`, `elif`, and implicit `else` path has been
tested in both the True and False directions.

## Test Cases Added

### Code Coverage Tests (21 tests)

- All three membership plans (monthly, quarterly, yearly)
- Senior discount (age ≥ 60)
- Student discount
- Senior overrides student (elif logic)
- Trainer add-on for monthly and yearly plans
- Invalid plan and underage exceptions
- Gym entry: active/inactive plan, before/after hours, women-only slot (F and M)
- BMI: underweight, normal, overweight, obese, invalid height

### Branch Coverage Tests (31 tests)

All of the above, plus:

- Boundary values: age exactly 14, hour exactly 5 and 22
- BMI boundaries: exactly 18.5, 25, and 30
- Explicit True and False paths for every conditional
- Negative height for BMI
- No-discount path (non-senior, non-student)
- No-trainer path

## Final Coverage Percentages

| Metric | Percentage |
|--------|-----------|
| Code (Line) Coverage | **100%** |
| Branch Coverage | **100%** |

## Screenshots

- Code coverage: `screenshots/code_coverage.png`
- Branch coverage: `screenshots/branch_coverage.png`

## Conclusion

By writing targeted test cases that cover all valid inputs, invalid inputs,
boundary values, exception paths, and both True/False outcomes of every decision
branch, we achieved 100% code coverage and 100% branch coverage for the
`gym_membership.py` module. This demonstrates that thorough testing requires
covering not just every line but every possible path through each conditional
statement.
