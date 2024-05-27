def flatten_tree(tree: dict, parent_key='') -> list[str]:
    """Flatten a nested dictionary tree into a list of paths."""
    flat_list = []
    for key, value in tree.items():
        # Construct the path
        path = f"{parent_key}/{key}" if parent_key else key
        # Check if the value is a non-empty dictionary
        if isinstance(value, dict) and value:
            # Recursively flatten the nested dictionary
            flat_list.extend(flatten_tree(value, path))
        else:
            # Add the path to the flat list
            flat_list.append(path)
    return flat_list