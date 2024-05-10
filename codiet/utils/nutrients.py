"""Utility functions for working with nutrient data."""

def ingredient_nutrient_data_is_complete(ingredient_nutrient_data: dict) -> bool:
    """Check if the nutrient data is complete."""
    if ingredient_nutrient_data["ntr_qty_value"] is None:
        return False
    if ingredient_nutrient_data["ing_qty_value"] is None:
        return False
    else: 
        return True

def get_missing_leaf_nutrient_names(nutrient_names: list[str], global_leaf_nutrient_names: list[str]) -> list[str]:
    """Returns a list of leaf nutrients that are missing from the leaf nutrients list."""
    missing_leaf_nutrients = []
    for nutrient in nutrient_names:
        if nutrient not in global_leaf_nutrient_names:
            missing_leaf_nutrients.append(nutrient)
    return missing_leaf_nutrients

def find_leaf_nutrients(data, leaf_nutrients=None) -> list[str]:
    """Recursively find all leaf nutrients in a nested dictionary."""
    # Initialise the list of leaf nutrients on the first call
    if leaf_nutrients is None:
        leaf_nutrients = []
    # Cycle through each nutrient,
    for key, value in data.items():
        # check if it has children
        if value.get("children"):
            # Recursively call the function with the children
            find_leaf_nutrients(value["children"], leaf_nutrients)
        else:
            # If no children, add the nutrient to the leaf_nutrients list
            leaf_nutrients.append(key)
    
    return leaf_nutrients