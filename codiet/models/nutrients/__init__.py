from .nutrient import Nutrient

def filter_leaf_nutrients(nutrients: dict[int, Nutrient]) -> dict[int, Nutrient]:
    """Filter out the leaf nutrients."""
    return {id: nutrient for id, nutrient in nutrients.items() if not nutrient.is_parent}