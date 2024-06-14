from typing import Any

def value_is_positive_number(value: Any) -> bool:
    """Check if a value is a positive number."""
    return isinstance(value, (int, float)) and value > 0