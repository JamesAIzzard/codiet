from fuzzywuzzy import process

def filter_text(text: str, all_names: list[str], count: int = 10) -> list[str]:
    """Returns a list of ingredient names that match the given name."""
    matches = process.extract(text, all_names, limit=count)
    return [match[0] for match in matches]  # Return only the names, not the scores

