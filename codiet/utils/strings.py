def convert_to_snake_case(name: str) -> str:
    """Convert a string to snake case."""
    # Replace spaces with underscores
    name = name.replace(" ", "_")
    # Replace hyphens with underscores
    name = name.replace("-", "_")
    # Convert to lowercase
    name = name.lower()
    return name