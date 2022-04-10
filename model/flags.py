import enum

from model.configs import FLAG_CONFIGS



def get_flag_name_from_string(flag_string: str) -> str:
    """Returns the flag name corresponding to the string text."""
    for flag_name, flag_params in FLAG_CONFIGS.items():
        if flag_params["string"] == flag_string:
            return flag_name
    raise ValueError("Flag name not recognised.")
