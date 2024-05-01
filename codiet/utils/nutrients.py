from codiet.db.database_service import DatabaseService

def get_missing_leaf_nutrients(nutrient_list: list[str], db_service: DatabaseService) -> list[str]:
    """Returns a list of leaf nutrients that are missing from the leaf nutrients list."""
    all_leaf_nutrients = db_service.fetch_all_leaf_nutrient_names()
    return [leaf_nutrient for leaf_nutrient in all_leaf_nutrients if leaf_nutrient not in nutrient_list]

def find_leaf_nutrients(data, leaf_nutrients=None) -> list[str]:
    """Recursively find all leaf nutrients in a nested dictionary."""
    # Initialize the list of leaf nutrients on the first call
    if leaf_nutrients is None:
        leaf_nutrients = []

    for key, value in data.items():
        # Check if the current item has children
        if value.get("children"):
            # Recursively call the function with the children
            find_leaf_nutrients(value["children"], leaf_nutrients)
        else:
            # If no children, add the nutrient to the leaf_nutrients list
            leaf_nutrients.append(key)

    return leaf_nutrients