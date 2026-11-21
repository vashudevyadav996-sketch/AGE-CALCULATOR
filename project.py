
from datetime import date
import calendar


def get_valid_date(prompt):
    while True:
        try:
            date_str = input(prompt).strip()
            parts = date_str.split("-")

            if len(parts) != 3:
                print("Invalid format! Please enter the date in DD-MM-YYYY format (e.g., 15-08-2005).")
                continue

            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            birth_date = date(year, month, day)

            if birth_date > date.today():
                print("Birth date cannot be in the future. Please try again.")
                continue

            return birth_date

        except ValueError:
            print("Invalid date! Please enter a valid calendar date.")


def calculate_age(birth_date, target_date=None):
    if target_date is None:
        target_date = date.today()

    years = target_date.year - birth_date.year
    months = target_date.month - birth_date.month
    days = target_date.day - birth_date.day

    # Borrow days from the previous month
    if days < 0:
        months -= 1

        prev_month = target_date.month - 1 if target_date.month > 1 else 12
        prev_year = target_date.year if target_date.month > 1 else target_date.year - 1

        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month

    # Borrow months from the previous year
    if months < 0:
        years -= 1
        months += 12

    total_days = (target_date - birth_date).days

    return years, months, days, total_days


def next_birthday_countdown(birth_date, today):
    next_bday_year = today.year

    try:
        next_bday = date(next_bday_year, birth_date.month, birth_date.day)
    except ValueError:
        # Handle February 29 in non-leap years
        next_bday = date(next_bday_year, 2, 28)

    if next_bday < today:
        next_bday_year += 1

        try:
            next_bday = date(next_bday_year, birth_date.month, birth_date.day)
        except ValueError:
            next_bday = date(next_bday_year, 2, 28)

    return (next_bday - today).days, next_bday


def main():
    print("=== PYTHON AGE CALCULATOR ===")

    dob = get_valid_date("Enter your Date of Birth (DD-MM-YYYY): ")

    today = date.today()

    years, months, days, total_days = calculate_age(dob, today)

    days_left, next_bday = next_birthday_countdown(dob, today)

    print("\n--- Result ---")

    print(f"Date of Birth   : {dob.strftime('%d-%m-%Y')} ({dob.strftime('%A')})")
    print(f"Current Date    : {today.strftime('%d-%m-%Y')}")
    print(f"Exact Age       : {years} years, {months} months, {days} days")
    print(f"Total Days Lived: {total_days:,} days")

    if days_left == 0:
        print("Today is your birthday! Happy Birthday!")
    else:
        print(f"Next Birthday   : {next_bday.strftime('%d-%m-%Y')} ({days_left} days remaining)")


if __name__ == "__main__":
    main()
