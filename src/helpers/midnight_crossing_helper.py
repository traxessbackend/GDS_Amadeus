from datetime import date, datetime
from pathlib import Path

datetime_format: str = "%Y-%m-%d %H:%M:%S.%f%z"


# Function to read the last checked day from a file
def read_last_checked_day(file: Path) -> datetime | None:
    checked_day: datetime | None = None
    if file.exists():
        try:
            checked_day = datetime.strptime(file.read_text().strip(), datetime_format)
        except Exception as exc:
            pass
    return checked_day


# Function to write the last checked day to a file
def write_last_checked_day(file: Path, day: datetime) -> bool:
    result: bool = False
    try:
        if not file.exists():
            file.touch()
        dt = day.strftime(datetime_format)
        file.write_text(dt)
        result = True
    except:
        pass
    return result


def days_difference(date1: datetime | date, date2: datetime | date):
    """
    Calculate the difference in days between two dates.

    Args:
        date1 (datetime): The first date
        date2 (datetime): The second date

    Returns:
        int: The difference in days between the two dates.
    """
    # Calculate the difference in days
    return abs((date1 - date2).days)
