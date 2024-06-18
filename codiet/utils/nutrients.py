"""Utility functions for working with nutrient data."""


def find_leaf_nutrient_names(
    nutrient_data: dict[str, dict], leaf_nutrient_names: list[str] | None = None
) -> list[str]:
    """Recursively find all leaf nutrients in a nested dictionary."""
    # Initialise the list of leaf nutrients on the first call
    if leaf_nutrient_names is None:
        leaf_nutrient_names = []
    # Cycle through each nutrient,
    for nutrient_name, nutrient_data in nutrient_data.items():
        # check if it has children
        if nutrient_data.get("children"):
            # Recursively call the function with the children
            find_leaf_nutrient_names(nutrient_data["children"], leaf_nutrient_names)
        else:
            # If no children, add the nutrient to the leaf_nutrients list
            leaf_nutrient_names.append(nutrient_name)
    return leaf_nutrient_names
