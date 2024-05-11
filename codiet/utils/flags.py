"""Utility functions for working with flags."""

def get_missing_flags(flag_list: list[str], global_flag_list: list[str]) -> list[str]:
    """Returns a list of flags that are on the global list but not in the flag list."""
    # Create a list to contain the missing flags
    missing_flags = []
    # Check each flag in the global list
    for flag in global_flag_list:
        # If the flag is not in the flag list, add it to the missing flags list
        if flag not in flag_list:
            missing_flags.append(flag)
    return missing_flags