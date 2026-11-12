# Lab 5: Reflection

**Name:** Darisi Anantha Venkata Sreeram  **SRN:** PES1UG24AM076

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the style issues — trailing whitespace, the missing blank line (E302), long lines, snake_case names and docstrings. The tool gives the exact line and the fix is mechanical; none of them change what the program does.

**Hardest:** the `eval()` call in `shortlist`. Bandit suggests `ast.literal_eval`, but that rejects `"500000 + 150000"` with a `ValueError`, so following the tool's hint literally would have broken the program. I had to decide what the function should really accept, and changed it to take the salary limit as a number. The silent `try/except: pass` in `updateStatus` also needed thought: simply deleting the `try` would crash the program on a database error, so I chose to catch only `sqlite3.Error`, roll back, and return `True`/`False` so the caller can see whether the update worked.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

There were no real false positives in this file — every Bandit finding was a genuine risk. Some findings were less accurate than they looked, though:

- **Bandit B608** only has *Medium* confidence because it guesses from string-built SQL. Here it was right (names with a quote broke the INSERT), but the same rule also flags safe queries that join constant strings.
- **Bandit B307's suggested fix** (`ast.literal_eval`) does not fit this code, as described above.
- **Pylint and Flake8 disagree on line length** (100 vs 79 characters), so a line could pass one tool and fail the other. That is a configuration difference, not a bug.

The tools also missed real bugs: none of them flagged that `",".join(row)` breaks on commas and NULLs, or that `main()` ran on import. I found those by reading the code.

## 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint in the editor while coding, and add a **pre-commit hook** that runs Flake8, Pylint and Bandit so a commit with new issues is blocked before it is made.
- **In CI:** run all three on every pull request (for example a GitHub Actions job) and fail the build if Bandit finds a Medium/High issue, Flake8 reports anything, or the Pylint score drops below 9.5.
- **Shared configuration:** keep one config file (`setup.cfg` / `pyproject.toml`) so everyone uses the same line length and rules, and require a written reason for any `# nosec` or `# pylint: disable` comment.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** no SQL injection and no `eval` — Bandit went from 2 Medium + 1 Low issues to none.
- **Robustness:** `shortlist` always returns a list, `update_status` reports failures instead of hiding them, the report file is always closed, and the CSV export handles commas and NULLs.
- **Readability:** consistent snake_case names, a docstring on every function and short lines. Pylint went from **4.47/10 to 10.00/10** and Flake8 from 8 warnings to 0.
- **Reusability:** the module can now be imported without running the demo.
