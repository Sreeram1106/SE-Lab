LOAN_DAYS = 14
FINE_PER_DAY = 2


def is_whole_number(text):
    """True if text contains only the digits 0-9 (no sign, no spaces)."""
    return text.isascii() and text.isdigit()


def parse_member_id(member_id):
    """Return (TYPE, number) for an ID like 'STU-1023', or None if invalid."""
    if not isinstance(member_id, str):
        return None
    parts = member_id.strip().split('-')
    if len(parts) != 2:
        return None
    member_type, number = parts[0].strip(), parts[1].strip()
    if not (member_type.isascii() and member_type.isalpha()):
        return None
    if not is_whole_number(number):
        return None
    try:
        return member_type.upper(), int(number)
    except ValueError:  # more digits than int() accepts
        return None


def total_fine(days_csv):
    """Return the fine for comma-separated days kept, or None if invalid."""
    if not isinstance(days_csv, str):
        return None
    fine = 0
    for part in days_csv.split(','):
        part = part.strip()
        if not is_whole_number(part):  # empty, text or negative value
            return None
        try:
            days = int(part)
        except ValueError:  # more digits than int() accepts
            return None
        if days > LOAN_DAYS:
            fine += (days - LOAN_DAYS) * FINE_PER_DAY
    return fine


def shelf_code(title):
    """Return the initials of the first two words in upper case, or None."""
    if not isinstance(title, str):
        return None
    words = title.split()
    if len(words) < 2:
        return None
    return (words[0][0] + words[1][0]).upper()


def main():
    print("==== Running parse_member_id ====")
    user_input = input("Enter a member ID (e.g. STU-1023): ")
    result = parse_member_id(user_input)
    if result is None:
        print("Invalid member ID. Use TYPE-NUMBER, e.g. STU-1023")
    else:
        print("Member Type and Number:", result)

    print("\n==== Running total_fine ====")
    user_input = input("Enter days kept for each book as CSV (e.g. 10,20,30): ")
    result = total_fine(user_input)
    if result is None:
        print("Invalid input. Enter whole numbers of days separated by commas")
    else:
        print("Total Fine:", result)

    print("\n==== Running shelf_code ====")
    user_input = input("Enter a book title with at least two words: ")
    result = shelf_code(user_input)
    if result is None:
        print("Invalid title. Enter at least two words")
    else:
        print("Shelf Code:", result)


if __name__ == "__main__":
    main()
