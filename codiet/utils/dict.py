def align_keys_with_template(template, child):
    """
    Ensure the top-level keys of the child dictionary match those of the template dictionary.
    Keys not in the template will be removed from the child, and keys in the template but not
    in the child will be added to the child. Where a key is added, the value will be taken from
    the template.

    Args:
    template (dict): The template dictionary with the desired keys.
    child (dict): The child dictionary to be aligned with the template.

    Returns:
    dict: The modified child dictionary with keys aligned to the template.
    """
    # Remove keys from child that are not in the template
    for key in list(child.keys()):
        if key not in template:
            print(f"Removing key {key} from datafile.")
            del child[key]

    # Add keys to child that are in the template but not in the child
    for key in template:
        if key not in child:
            print(f"Adding key {key}: {template[key]} to datafile.")
            child[key] = template[key]

    return child
