from codiet.models.ingredient import Ingredient

class Recipe:
    def __init__(self):
        self.name: str | None = None
        self.id: int | None = None
        self.description: str | None = None
        self.instructions: str | None = None
        self.ingredients: dict[str, dict] = {}
        self.serve_times: list[str] = []
        self.recipe_types: list[str] = []

    def add_ingredient(
            self, 
            ingredient: Ingredient,
            ingredient_qty: float | None = None,
            ingredient_qty_unit: str = "g",
            ingredient_qty_utol: float | None = None,
            ingredient_qty_ltol: float | None = None
        ) -> None:
        """Add an ingredient to the recipe."""
        # Assert the ingredient has a name
        assert ingredient.name is not None
        # Check if the ingredient is already in the recipe
        for existing_ingredient in self.ingredients:
            if self.ingredients[existing_ingredient]["id"] == ingredient.id:
                return
        # Add the ingredient to the recipe
        self.ingredients[ingredient.name] = {
            "id": ingredient.id,
            "qty": ingredient_qty,
            "qty_unit": ingredient_qty_unit,
            "qty_utol": ingredient_qty_utol,
            "qty_ltol": ingredient_qty_ltol
        }

    def remove_ingredient(self, ingredient_id: int) -> None:
        """Remove an ingredient from the recipe."""
        # Cycle through each ingredient
        for ingredient in self.ingredients:
            # Check if the ingredient ID matches the ingredient ID to remove
            if self.ingredients[ingredient]["id"] == ingredient_id:
                # Remove the ingredient from the recipe
                del self.ingredients[ingredient]
                return
        # Raise a value error if the ingredient is not in the recipe
        raise ValueError("Ingredient not in recipe")