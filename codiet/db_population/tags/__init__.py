import json
import os

from codiet.model.tags.tag import Tag

GLOBAL_TAGS_FILENAME = 'global_tags.json'
GLOBAL_TAGS_FILEPATH = os.path.join(os.path.dirname(__file__), GLOBAL_TAGS_FILENAME)

_cached_global_tags: set[Tag] | None = None

def read_global_tags_from_json(global_tags_filepath: str=GLOBAL_TAGS_FILEPATH) -> set[Tag]:
    """Reads the tags JSON datafile and returns the data as a set of tags."""
    global _cached_global_tags
    
    if _cached_global_tags is not None:
        return _cached_global_tags

    tags = set()
    with open(global_tags_filepath, 'r') as f:
        data: list[str] = json.load(f)

    for tag_name in data:
        tag = Tag(name=tag_name)
        tags.add(tag)

    _cached_global_tags = tags
    
    return tags