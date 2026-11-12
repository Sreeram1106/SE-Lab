"""Code (line) coverage tests for library_fines.py.

Starting from the two starter tests, one test was added for each line
that `coverage report -m` listed as missing, until every line of
library_fines.py runs at least once.
"""
import pytest

from library_fines import can_borrow, late_fine, renewal_status


# ----- Starter tests -----

def test_returned_on_time():
    assert late_fine("student", 10, False) == 0


def test_can_borrow():
    assert can_borrow(1, 0, "student") is True


# ----- late_fine -----

def test_unknown_member_raises():
    with pytest.raises(ValueError, match="unknown member"):
        late_fine("visitor", 5, False)


def test_negative_days_raises():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_faculty_long_overdue_damaged_book():
    # Faculty loan is 30 days: 270 days late * 1 = 270, capped at 200,
    # plus 150 for the damaged book.
    assert late_fine("faculty", 300, True) == 350


# ----- can_borrow -----

def test_pending_fine_over_100_blocks_borrowing():
    assert can_borrow(0, 150, "student") is False


def test_faculty_under_limit_can_borrow():
    assert can_borrow(5, 0, "faculty") is True


# ----- renewal_status -----

def test_renewal_denied_when_reserved():
    assert renewal_status(0, True, 5) == "denied"


def test_renewal_limit_reached():
    assert renewal_status(2, False, 5) == "limit reached"


def test_renewal_refused_when_overdue():
    assert renewal_status(1, False, -1) == "overdue"


def test_renewal_granted():
    assert renewal_status(0, False, 3) == "renewed"
