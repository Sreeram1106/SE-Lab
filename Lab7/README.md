# Lab 7 — Fuzzing for Input Validation Bugs (Submission)

- **SRN:** PES1UG24AM076
- **Name:** Darisi Anantha Venkata Sreeram
- **Assigned repo:** [L6_L7_14_library_fines](https://github.com/SETAPESU26/L6_L7_14_library_fines) (Lab 7 folder)

## Deliverables

| Deliverable | File |
|-------------|------|
| PDF document with the screenshots | `PES1UG24AM076_Lab7.pdf` |
| Fixed application script | `library_fines.py` |
| Updated Hypothesis test file | `test_library_fines.py` |

## Results

| Run | Result |
|-----|--------|
| Buggy app, invalid input (`STU1023`) | Crashes with `ValueError` |
| Fuzz tests on buggy code | **4 failed, 3 passed** |
| Fixed app, same inputs | Valid input unchanged; invalid input gives a clear message |
| Fuzz tests on fixed code | **7 passed** |

## Bugs found by fuzzing

| Function | Failing input found by Hypothesis | Error | Fix |
|----------|-----------------------------------|-------|-----|
| `parse_member_id` | `None` | `AttributeError` | Return `None` if the input is not a string |
| `parse_member_id` | `''` (no `-`) | `ValueError` (unpack) | Require exactly two parts around `-` |
| `parse_member_id` | `'-'` | `ValueError` (`int('')`) | Require a letters-only type and a digits-only number |
| `total_fine` | `None` | `AttributeError` | Return `None` if the input is not a string |
| `total_fine` | `''` / `'1,,3'` | `ValueError` (`int('')`) | Check every value is a whole number before `int()` |
| `total_fine` | `'-1'` | No crash, but returned `0` | Negative days are rejected (returns `None`) |
| `shelf_code` | `None` | `AttributeError` | Return `None` if the input is not a string |
| `shelf_code` | `''` / one word | `IndexError` | Return `None` if there are fewer than two words |

Invalid input now returns `None` instead of raising, and `main()` prints a message
for it. `int()` is also wrapped in `try/except`, because Python refuses to convert
strings longer than 4300 digits.

## Tests (`test_library_fines.py`)

- **Fuzz (no-crash) tests:** each function gets random Unicode text or `None`.
- **Property tests:**
  - Valid IDs like `abc-42` parse to `('ABC', 42)`.
  - `total_fine` matches the rule of 2 per day after 14 days.
  - Any negative day is rejected.
  - `shelf_code` returns the initials of the first two words.

## How to run

```bash
pip install hypothesis pytest
python library_fines.py
pytest test_library_fines.py
```

The screenshots used the sample inputs in `inputs/` (fed in with
`cmd /c "python library_fines.py < inputs\valid.txt"`). The `screenshots/` folder has
each screenshot as a PNG along with the same output as text.
