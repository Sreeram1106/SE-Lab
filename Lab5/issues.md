# Lab 5: Identified Issues — `recruitment_tracker.py`

**Name:** Darisi Anantha Venkata Sreeram  **SRN:** PES1UG24AM076
**Repo:** L5_14_recruitment_tracker

Tools: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.5.0 (Python 3.11.9).
Line numbers refer to the **original** file. Reports are in `reports/before/` and `reports/after/`.

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.47/10, 21 messages | **10.00/10**, 0 messages |
| Bandit | 3 issues (2 Medium, 1 Low) | **No issues identified** |
| Flake8 | 8 warnings | **0 warnings** (empty report) |

## Issue table (high and medium severity first)

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | SQL injection — Bandit **B608** (Medium) | Security | 8 | `addApplicant` built the INSERT with an f-string. A name like `O'Brien` breaks the query, and crafted input can run extra SQL. | Parameterised query with `?` placeholders; values passed as a tuple to `conn.execute`. |
| 2 | Use of `eval` — Bandit **B307** (Medium), Pylint **W0123** | Security | 14 | `shortlist` ran `eval(salary_rule)`, which executes any Python string passed in (e.g. `__import__('os').remove(...)`). | `shortlist` now takes `max_salary` as a number; `main()` passes `500000 + 150000` directly. (`ast.literal_eval`, Bandit's suggestion, rejects the `+`, so it would not work here.) |
| 3 | `try/except: pass` on a broad `Exception` — Bandit **B110** (Low), Pylint **W0718** | Bug | 25–29 | Every database error in `updateStatus` was silently ignored, so callers could not tell that an update failed. Updating a non-existent id also failed silently. | Catch only `sqlite3.Error`, roll back, print the error and return `False`; return `True` only when exactly one row was updated (`cursor.rowcount == 1`). |
| 4 | Inconsistent return — Pylint **R1710** | Bug | 12–21 | `shortlist` returned a list when someone matched but `None` when nobody did, so code like `len(shortlist(...))` would crash. | Always return a list (list comprehension), empty when no applicant qualifies. |
| 5 | File not opened with `with`, no encoding — Pylint **R1732**, **W1514** | Bug | 32–35 | If writing failed, `f.close()` was never reached and the file handle leaked; the encoding depended on the OS. | `with open(path, "w", encoding="utf-8", newline="")` so the file is always closed. |
| 6 | Hand-built CSV (found in code review, no tool flagged it) | Bug | 34 | `",".join(row)` produces a broken row if a name contains a comma, and raises `TypeError` if any field is NULL. | Write rows with `csv.writer`, which quotes fields correctly. |
| 7 | Unused variable — Pylint **W0612**, Flake8 **F841** | Code smell | 15 | `total_seen` was computed and never used. | Removed. |
| 8 | Function names not snake_case — Pylint **C0103** | Style | 7, 24, 31, 38 | `addApplicant`, `updateStatus`, `exportReport`, `countByStatus` break PEP 8 naming. | Renamed to `add_applicant`, `update_status`, `export_report`, `count_by_status`. |
| 9 | Missing docstrings — Pylint **C0114**, **C0116** | Style | 1, 7, 12, 24, 31, 38, 42 | No module or function docstrings. | Added a module docstring and one per function. |
| 10 | Line too long — Flake8 **E501**, Pylint **C0301** | Style | 4, 8, 13, 26, 39 | Lines of 93–140 characters (Flake8 limit 79, Pylint 100). | Wrapped SQL strings and call arguments. |
| 11 | Trailing whitespace — Flake8 **W291**, Pylint **C0303** | Style | 15 | Spaces after `len(rows)`. | Removed (the line was deleted with #7). |
| 12 | Missing blank lines — Flake8 **E302** | Style | 31 | Only one blank line before `def exportReport`. | Added the second blank line. |
| 13 | Demo runs on import (found in code review) | Design | 52 | `main()` was called at module level, so importing the file ran the demo and wrote a CSV. | Moved the call under `if __name__ == "__main__":`. |

## Commits

| Commit | What it fixes |
|--------|---------------|
| Fix Bandit security issues | #1, #2, #3 |
| Fix Pylint issues (score 4.47 -> 10.00) | #4–#9, #11, #13, and the Pylint part of #10 |
| Fix Flake8 style issues | #12 and the remaining E501 lines of #10 |
