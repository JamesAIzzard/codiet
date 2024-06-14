class IngredientNutrientQuantity:
    """Class to represent an ingredient nutrient."""

    def __init__(self,
        global_nutrient_id: int,
        ingredient_id: int,
        ntr_mass_value: float | None = None,
        ntr_mass_unit: str = "g",
        ing_qty_value: float | None = None,
        ing_qty_unit: str = "g",
    ):
        self.global_nutrient_id = global_nutrient_id
        self.ingredient_id = ingredient_id
        self.nutrient_mass_value = ntr_mass_value
        self.nutrient_mass_unit = ntr_mass_unit
        self.ingredient_quantity_value = ing_qty_value
        self.ingredient_quantity_unit = ing_qty_unit
