class IngredientQuantity:
    """Class to represent an ingredient quantity."""

    def __init__(
        self,
        id: int,
        ingredient_id: int,
        recipe_id: int,
        qty_value: float | None = 0.0,
        qty_unit_id: int|None = None,
        qty_utol: float | None = 0.0,
        qty_ltol: float | None = 0.0,
    ):
        """Initialises the class.
        Args:
            id (int): The ID of the ingredient quantity.
            ingredient_id (int): The ID of the ingredient.
            qty_value (float, optional): The quantity value. Defaults to 0.0.
            qty_unit_id (int, optional): The quantity unit ID. Defaults to None.
            qty_utol (float, optional): The upper tolerance. Defaults to 0.0.
            qty_ltol (float, optional): The lower tolerance. Defaults to 0.0.
        """
        self.id = id
        self.recipe_id = recipe_id
        self.ingredient_id = ingredient_id
        self.qty_value = qty_value
        self.qty_unit_id = qty_unit_id
        self.upper_tol = qty_utol
        self.lower_tol = qty_ltol