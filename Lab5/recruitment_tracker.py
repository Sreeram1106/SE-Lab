"""Applicant tracking system for an HR team.

Stores job applicants in an in-memory SQLite database, shortlists
candidates for a role against a salary budget, updates their hiring
status and exports a CSV report.
"""
import csv
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE applicants (id INTEGER PRIMARY KEY, name TEXT, role TEXT, "
    "expected_salary INTEGER, status TEXT)"
)


def add_applicant(name, role, expected_salary, status="applied"):
    """Insert a new applicant into the database."""
    conn.execute(
        "INSERT INTO applicants (name, role, expected_salary, status) "
        "VALUES (?, ?, ?, ?)",
        (name, role, expected_salary, status),
    )
    conn.commit()


def shortlist(role, max_salary):
    """Return the names of applicants for a role within the salary budget.

    Always returns a list, which is empty when nobody qualifies.
    """
    rows = conn.execute(
        "SELECT name, expected_salary FROM applicants WHERE role = ?", (role,)
    ).fetchall()
    return [name for name, salary in rows if salary <= max_salary]


def update_status(applicant_id, status):
    """Set an applicant's hiring status.

    Returns True if exactly one applicant was updated, otherwise False.
    """
    try:
        cursor = conn.execute(
            "UPDATE applicants SET status = ? WHERE id = ?",
            (status, applicant_id),
        )
        conn.commit()
    except sqlite3.Error as error:
        conn.rollback()
        print(f"Could not update applicant {applicant_id}: {error}")
        return False
    return cursor.rowcount == 1


def export_report(path):
    """Write every applicant's name, role and status to a CSV file."""
    with open(path, "w", encoding="utf-8", newline="") as report:
        writer = csv.writer(report)
        writer.writerows(
            conn.execute("SELECT name, role, status FROM applicants")
        )


def count_by_status(status):
    """Return how many applicants currently have the given status."""
    return conn.execute(
        "SELECT COUNT(*) FROM applicants WHERE status = ?", (status,)
    ).fetchone()[0]


def main():
    """Run a short demonstration of the tracker."""
    add_applicant("Nina", "analyst", 600000)
    add_applicant("Omar", "analyst", 750000, "interview")
    add_applicant("Priya", "developer", 900000)
    update_status(1, "interview")
    print(shortlist("analyst", 500000 + 150000))
    export_report("applicants_report.csv")
    print(count_by_status("interview"), "in interview")


if __name__ == "__main__":
    main()
