import json
import os

from codiet.models.flags.flag import Flag

GLOBAL_FLAGS_FILENAME = 'global_flags.json'
GLOBAL_FLAGS_FILEPATH = os.path.join(os.path.dirname(__file__), GLOBAL_FLAGS_FILENAME)

_cached_global_flags: set[Flag] | None = None

def read_global_flags_from_json(global_flags_filepath: str=GLOBAL_FLAGS_FILEPATH) -> set[Flag]:
    """Reads the flags JSON datafile and returns the data as a set of flags."""
    global _cached_global_flags
    
    if _cached_global_flags is not None:
        return _cached_global_flags

    flags = set()
    with open(global_flags_filepath, 'r') as f:
        data: list[str] = json.load(f)

    for flag_name in data:
        flag = Flag(flag_name=flag_name)
        flags.add(flag)

    _cached_global_flags = flags
    return flags
