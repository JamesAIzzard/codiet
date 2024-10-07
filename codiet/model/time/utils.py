from datetime import time

def parse_time_string(time_string: str) -> time:
    hours, minutes = map(int, time_string.split(":"))
    return time(hours, minutes)