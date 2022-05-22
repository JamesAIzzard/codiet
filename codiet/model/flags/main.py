from codiet import data

def flag_string_to_name(flag_string: str) -> str:
    """Returns the flag name corresponding to the string text."""
    for fn, fs in data.flags.get_flag_names_and_strings().items():
        if fs == flag_string:
            return fn
    raise ValueError("Flag name not recognised.")