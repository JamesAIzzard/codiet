import json
import os
from typing import Any

from codiet.utils.map import Map
from codiet.model.nutrients.nutrient import Nutrient

GLOBAL_NUTRIENTS_FILENAME = 'global_nutrients.json'
GLOBAL_NUTRIENTS_FILEPATH = os.path.join(os.path.dirname(__file__), GLOBAL_NUTRIENTS_FILENAME)

_cached_global_nutrients: set[Nutrient] | None = None

def read_global_nutrients_from_json(global_nutrients_filepath: str = GLOBAL_NUTRIENTS_FILEPATH) -> set[Nutrient]:
    """Reads the nutrients JSON datafile and returns the data as a set of all nutrients."""
    global _cached_global_nutrients

    if _cached_global_nutrients is not None:
        return _cached_global_nutrients

    with open(global_nutrients_filepath, 'r') as f:
        nutrients_data = json.load(f)

    def create_nutrient_tree(name: str, data: dict[str, Any], parent: Nutrient|None = None) -> tuple[Nutrient, set[Nutrient]]:
        aliases = set(data.get('aliases', []))
        nutrient = Nutrient(nutrient_name=name, aliases=aliases, parent=parent)
        all_nutrients = {nutrient}

        children = data.get('children', {})
        for child_name, child_data in children.items():
            child_nutrient, child_nutrients = create_nutrient_tree(child_name, child_data, parent=nutrient)
            nutrient._children._add(child_nutrient)
            all_nutrients.update(child_nutrients)

        return nutrient, all_nutrients

    _cached_global_nutrients = set()
    for name, data in nutrients_data.items():
        _, nutrients = create_nutrient_tree(name, data)
        _cached_global_nutrients.update(nutrients)

    return _cached_global_nutrients

def global_name_nutrient_map() -> Map[str, Nutrient]:
    """Creates a map of nutrient names to nutrient objects."""
    nutrients = read_global_nutrients_from_json()
    
    name_nutrient_map = Map()
    for nutrient in nutrients:
        name_nutrient_map[nutrient.nutrient_name] = nutrient

    return name_nutrient_map
