from datetime import datetime


def convert_datetime_to_time_string(dt: datetime) -> str:
    """Convert a datetime object to a time string."""
    return dt.strftime("%H:%M")

def convert_time_string_to_datetime(time_string: str) -> datetime:
    """Convert a time string to a datetime object."""
    return datetime.strptime(time_string, "%H:%M")

def convert_datetime_interval_to_time_string_interval(
    interval: tuple[datetime, datetime]
) -> str:
    """Convert a datetime interval to a time string."""
    return f"{convert_datetime_to_time_string(interval[0])} \
        - {convert_datetime_to_time_string(interval[1])}"

def convert_time_string_interval_to_datetime_interval(
    interval: str
) -> tuple[datetime, datetime]:
    """Convert a time string interval to a datetime interval."""
    # Strip any whitespace from anywhere in the string
    interval = interval.replace(" ", "")
    # Split the string based on the hyphen
    start, end = interval.split("-")
    # Convert the start and end times to datetime objects and return as tuple
    return convert_time_string_to_datetime(start), convert_time_string_to_datetime(end)
