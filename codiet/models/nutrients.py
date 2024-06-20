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
        nutrient: Nutrient,
        ingredient_id: int,
        ntr_mass_value: float | None = None,
        ntr_mass_unit_id: int | None = None,
        ing_qty_value: float | None = None,
        ing_qty_unit_id: int | None = None,
    ):
        self.id = id
        self.nutrient = nutrient
        self.ingredient_id = ingredient_id
        self.nutrient_mass_value = ntr_mass_value
        self.nutrient_mass_unit_id = ntr_mass_unit_id
        self.ingredient_quantity_value = ing_qty_value
        self.ingredient_quantity_unit_id = ing_qty_unit_id
