# Lab 5 — Static Code Analysis (Submission)

- **SRN:** PES1UG24AM076
- **Name:** Darisi Anantha Venkata Sreeram
- **Assigned repo:** [L5_14_recruitment_tracker](https://github.com/SETAPESU26/L5_14_recruitment_tracker)

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.47/10 | 10.00/10 |
| Bandit | 3 issues (2 Medium, 1 Low) | No issues |
| Flake8 | 8 warnings | 0 warnings |

## Files

- `recruitment_tracker.py` — cleaned version of the program.
- `issues.md` — table of the issues found and how each was fixed.
- `reflection.md` — answers to the reflection questions.
- `reports/before/` — `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` for the original script.
- `reports/after/` — the same three reports after the fixes (the Flake8 report is empty because no issues remain).

## Fix commits

1. **Lab 5: Fix Bandit security issues** — SQL injection, `eval()`, `try/except/pass`.
2. **Lab 5: Fix Pylint issues (score 4.47 -> 10.00)** — naming, docstrings, return values, file handling.
3. **Lab 5: Fix Flake8 style issues** — line length and blank lines.

---

# Lab 5: Static Code Analysis — Applicant Tracking System

**Your file:** `recruitment_tracker.py`

Follow the lab handout for the full instructions.

## About the program

A hiring tracker for an HR team. It stores job applicants in an SQLite database, shortlists candidates for a role against a salary budget, updates their hiring status and exports a report.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:
   ```bash
   python recruitment_tracker.py
   ```
   It runs a short demonstration and may create a small output file in the current folder, so run it from a folder you don't mind adding files to.

2. **Install the tools:**
   ```bash
   pip install pylint bandit flake8
   ```

3. **Run the analysis** and save the reports:
   ```bash
   pylint recruitment_tracker.py > pylint_report.txt
   bandit -r recruitment_tracker.py > bandit_report.txt
   flake8 recruitment_tracker.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ... | ... | ... | ... | ... |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

1. `recruitment_tracker.py`: your cleaned version, with at least 4 issues fixed.
2. `issues.md`: the completed issue table.
3. `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.
