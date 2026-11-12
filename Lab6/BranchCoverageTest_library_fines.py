"""Branch coverage tests for library_fines.py.

Every decision (if / elif) in library_fines.py is tested for both its
True and its False outcome. Where a condition compares numbers, the
tests sit right on the boundary where the branch flips.
"""
import pytest

from library_fines import DAILY_FINE, can_borrow, late_fine, renewal_status


# ===================== late_fine =====================

# Decision: member not in DAILY_FINE
@pytest.mark.parametrize("member", ["visitor", "", "Student"])
def test_unknown_member_raises(member):
    with pytest.raises(ValueError, match="unknown member"):
        late_fine(member, 5, False)


@pytest.mark.parametrize("member", sorted(DAILY_FINE))
def test_known_member_accepted(member):
    assert late_fine(member, 0, False) == 0


# Decision: days_kept < 0
def test_negative_days_raises():
    with pytest.raises(ValueError, match="invalid days"):
        late_fine("student", -1, False)


def test_zero_days_is_valid():
    assert late_fine("student", 0, False) == 0


# Decisions: member == "faculty" (30-day loan, else 14) and overdue > 0
def test_faculty_on_last_day_of_loan_pays_nothing():
    assert late_fine("faculty", 30, False) == 0


def test_faculty_one_day_late():
    assert late_fine("faculty", 31, False) == 1


def test_student_on_last_day_of_loan_pays_nothing():
    assert late_fine("student", 14, False) == 0


def test_student_one_day_late():
    assert late_fine("student", 15, False) == 2


def test_guest_one_day_late():
    assert late_fine("guest", 15, False) == 5


# Decision: fine > 200 (cap)
def test_fine_of_exactly_200_is_not_capped():
    # guest: 40 days late * 5 = 200, which is not more than 200
    assert late_fine("guest", 54, False) == 200


def test_fine_just_over_200_is_capped():
    # guest: 41 days late * 5 = 205 -> 200
    assert late_fine("guest", 55, False) == 200


def test_large_fine_is_capped():
    # guest: 86 days late * 5 = 430 -> 200
    assert late_fine("guest", 100, False) == 200


# Decision: is_damaged
def test_damaged_book_returned_on_time_costs_150():
    assert late_fine("student", 10, True) == 150


def test_damaged_book_adds_150_to_late_fine():
    assert late_fine("student", 15, True) == 152


def test_damaged_book_adds_150_after_cap():
    assert late_fine("faculty", 300, True) == 350


# ===================== can_borrow =====================

# Decision: pending_fine > 100
def test_pending_fine_of_exactly_100_still_allowed():
    assert can_borrow(0, 100, "student") is True


def test_pending_fine_over_100_blocks_borrowing():
    assert can_borrow(0, 101, "student") is False


def test_pending_fine_blocks_faculty_too():
    assert can_borrow(0, 150, "faculty") is False


# Decision: member == "faculty" (limit 10, else limit 3)
@pytest.mark.parametrize("books_held, expected", [(9, True), (10, False)])
def test_faculty_book_limit(books_held, expected):
    assert can_borrow(books_held, 0, "faculty") is expected


@pytest.mark.parametrize("member", ["student", "guest"])
@pytest.mark.parametrize("books_held, expected", [(2, True), (3, False)])
def test_other_members_book_limit(member, books_held, expected):
    assert can_borrow(books_held, 0, member) is expected


# ===================== renewal_status =====================

# Decision: has_reservation
def test_reserved_book_is_denied():
    assert renewal_status(0, True, 5) == "denied"


def test_reservation_checked_before_limit_and_overdue():
    assert renewal_status(2, True, -3) == "denied"


# Decision: times_renewed >= 2
def test_one_renewal_so_far_is_allowed():
    assert renewal_status(1, False, 5) == "renewed"


def test_two_renewals_reaches_limit():
    assert renewal_status(2, False, 5) == "limit reached"


def test_limit_checked_before_overdue():
    assert renewal_status(3, False, -1) == "limit reached"


# Decision: days_left < 0
def test_overdue_book_is_not_renewed():
    assert renewal_status(1, False, -1) == "overdue"


def test_book_due_today_is_renewed():
    assert renewal_status(0, False, 0) == "renewed"
