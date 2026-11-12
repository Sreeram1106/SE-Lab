# Lab 6 — Code and Branch Coverage Analysis (Submission)

- **SRN:** PES1UG24AM076
- **Name:** Darisi Anantha Venkata Sreeram
- **Assigned repo:** [L6_L7_14_library_fines](https://github.com/SETAPESU26/L6_L7_14_library_fines)

## Results (`library_fines.py`)

| Test file | Tests | Line coverage | Branch coverage |
|-----------|-------|---------------|-----------------|
| `CodeCoverageTest_library_fines.py` | 11 passed | **100%** (32/32 statements) | 98% (21/22 branches, missing `17->19`) |
| `BranchCoverageTest_library_fines.py` | 35 passed | **100%** (32/32 statements) | **100%** (22/22 branches) |

The code coverage tests run every line, but they never take the path where an
overdue fine stays **at or below** the 200 cap (line 17 false, jumping to line 19).
Line coverage cannot see this; branch coverage reports it as `17->19`. The branch
coverage tests check every `if` / `elif` both ways, using boundary values such as
30 vs 31 days for faculty, a fine of exactly 200 vs 205, a pending fine of 100 vs 101,
2 vs 3 books held and a book due today (`days_left == 0`).

## Commands

```bash
pip install coverage pytest

coverage run -m pytest CodeCoverageTest_library_fines.py
coverage report -m
coverage run --branch -m pytest CodeCoverageTest_library_fines.py
coverage report -m

coverage run -m pytest BranchCoverageTest_library_fines.py
coverage report -m
coverage run --branch -m pytest BranchCoverageTest_library_fines.py
coverage report -m
```

## Files

| File | Description |
|------|-------------|
| `library_fines.py` | The module under test (unchanged) |
| `test_library_fines.py` | Starter test file (unchanged) |
| `CodeCoverageTest_library_fines.py` | Test cases for code (line) coverage |
| `BranchCoverageTest_library_fines.py` | Test cases for branch coverage |
| `screenshots/code_coverage.png` | Terminal output for the code coverage tests |
| `screenshots/branch_coverage.png` | Terminal output for the branch coverage tests |
| `screenshots/*_output.txt` | The same terminal output as plain text |

## Commits

1. **Lab 6: Add code coverage test cases** — `CodeCoverageTest_library_fines.py` and its screenshot.
2. **Lab 6: Add branch coverage test cases** — `BranchCoverageTest_library_fines.py` and its screenshot.

---

## About the module

A small Python module that works out late return fines by member type, checks whether a member can borrow more books and decides if a book can be renewed.
