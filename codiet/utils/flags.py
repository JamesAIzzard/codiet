from codiet.db.database_service import DatabaseService

def get_missing_flags(flag_list: list[str], global_flag_list: list[str]) -> list[str]:
    """Returns a list of flags that are missing from the global flag list."""
    missing_flags = []
    for flag in flag_list:
        if flag not in global_flag_list:
            missing_flags.append(flag)
    return missing_flags