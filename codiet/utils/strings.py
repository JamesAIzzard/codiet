def string_is_populated(string: str) -> bool:
    """Check if a string is populated."""
    return bool(string and string.strip())

def convert_to_snake_case(name: str) -> str:
    """Convert a string to snake case."""
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    # Replace hyphens with underscores
    name = name.replace("-", "_")
    # Convert to lowercase
    name = name.lower()
    return name

def convert_snake_case_to_title_case(name: str) -> str:
    """Convert a snake case string to title case."""
    # Replace underscores with spaces
    name = name.replace("_", " ")
    # Capitalize the first letter of each word
    name = name.title()
    return name