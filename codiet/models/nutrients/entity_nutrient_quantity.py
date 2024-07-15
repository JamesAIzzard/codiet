class EntityNutrientQuantity:
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