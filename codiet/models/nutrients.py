class Nutrient:
    """Class to represent a nutrient."""

    def __init__(
        self,
        id: int,
        nutrient_name: str,
        aliases: list[str] | None = None,
        parent_id: int | None = None,
        child_ids: list[int] | None = None,
    ):
        self.id = id
        self.nutrient_name = nutrient_name
        self.aliases = aliases if aliases is not None else []
        self.parent_id = parent_id
        self.child_ids = child_ids if child_ids is not None else []

    @property
    def is_parent(self) -> bool:
        """Returns True if the nutrient is a parent."""
        return len(self.child_ids) > 0
    
    @property
    def is_child(self) -> bool:
        """Returns True if the nutrient is a child."""
        return self.parent_id is not None

class IngredientNutrientQuantity:
    """Class to represent an ingredient nutrient."""

    def __init__(
        self,
        id: int,
        nutrient_id: int,
        ingredient_id: int,
        ntr_mass_unit_id: int,
        ntr_mass_value: float | None = None,
        ing_grams_value: float | None = None,
    ):
        """Initialise the class.
        Args:
            id (int): The id of the ingredient nutrient quantity.
            nutrient_id (int): The id of the nutrient.
            ingredient_id (int): The id of the ingredient.
            ntr_mass_unit_id (int): The id of the mass unit of the nutrient.
            ntr_mass_value (float, optional): The mass value of the nutrient. Defaults to None.
            ing_grams_value (float, optional): The grams value of the ingredient.
                Defaults to None.
        """
        self.id = id
        self.nutrient_id = nutrient_id
        self.ingredient_id = ingredient_id
        self.nutrient_mass_value = ntr_mass_value
        self.nutrient_mass_unit_id = ntr_mass_unit_id
        self.ing_grams_value = ing_grams_value

def filter_leaf_nutrients(nutrients: dict[int, Nutrient]) -> dict[int, Nutrient]:
    """Filter out the leaf nutrients."""
    return {id: nutrient for id, nutrient in nutrients.items() if not nutrient.is_parent}