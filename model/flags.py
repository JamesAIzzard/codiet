import model

def flag_string_to_flag_name(flag_string: str) -> str:
    """Returns the flag name corresponding to the string text."""
    for flag_name, flag_params in model.configs.FLAG_CONFIGS.items():
        if flag_params["string"] == flag_string:
            return flag_name
    raise ValueError("Flag name not recognised.")
