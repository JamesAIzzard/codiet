class IngredientNutrientQuantity:
    """Class to represent an ingredient nutrient."""

    def __init__(self,
        name: str,
        ntr_mass_value: float | None = None,
        ntr_mass_unit: str = "g",
        ing_qty_value: float | None = None,
        ing_qty_unit: str = "g",
    ):
        self.name = name
        self.nutrient_mass = ntr_mass_value
        self.nutrient_mass_unit = ntr_mass_unit
        self.ingredient_quantity = ing_qty_value
        self.ingredient_quantity_unit = ing_qty_unit
