from hypothesis import given, strategies as st
from library_fines import parse_member_id, total_fine, shelf_code


# ---------- Fuzz tests: no input may crash a function ----------

@given(st.text() | st.none())
def test_parse_member_id_no_crash(s):
    try:
        parse_member_id(s)
    except Exception as e:
        assert False, f"parse_member_id crashed with: {e!r}"


@given(st.text() | st.none())
def test_total_fine_no_crash(s):
    try:
        total_fine(s)
    except Exception as e:
        assert False, f"total_fine crashed with: {e!r}"


@given(st.text() | st.none())
def test_shelf_code_no_crash(s):
    try:
        shelf_code(s)
    except Exception as e:
        assert False, f"shelf_code crashed with: {e!r}"


# ---------- Property tests: valid input gives the right answer ----------

@given(st.from_regex(r"[A-Za-z]{1,5}", fullmatch=True),
       st.integers(min_value=0, max_value=10**6))
def test_parse_member_id_valid_round_trip(member_type, number):
    member_id = f"{member_type}-{number}"
    assert parse_member_id(member_id) == (member_type.upper(), number)


@given(st.lists(st.integers(min_value=0, max_value=365), min_size=1))
def test_total_fine_matches_rule(days):
    days_csv = ",".join(str(d) for d in days)
    expected = sum((d - 14) * 2 for d in days if d > 14)
    assert total_fine(days_csv) == expected


@given(st.lists(st.integers(min_value=0, max_value=365)),
       st.integers(min_value=-365, max_value=-1))
def test_total_fine_rejects_negative_days(days, negative_day):
    days_csv = ",".join(str(d) for d in days + [negative_day])
    assert total_fine(days_csv) is None


@given(st.lists(st.from_regex(r"[A-Za-z]{1,10}", fullmatch=True),
                min_size=2, max_size=6))
def test_shelf_code_uses_first_two_initials(words):
    title = " ".join(words)
    assert shelf_code(title) == (words[0][0] + words[1][0]).upper()
