from datetime import datetime

from codiet.models.ingredients import IngredientQuantity

class Recipe:
    def __init__(self):
        self.name: str | None = None
        self.id: int | None = None
        self.description: str | None = None
        self.instructions: str | None = None
        self._ingredients: dict[str, IngredientQuantity] = {}
        self._serve_times: list[tuple[datetime, datetime]] = []
        self._recipe_types: list[str] = []

    @property
    def serve_times(self) -> list[tuple[datetime, datetime]]:
        """Get the serve times for the recipe."""
        return self._serve_times
    
    @serve_times.setter
    def serve_times(self, serve_times: list[tuple[datetime, datetime]]) -> None:
        """Set the serve times for the recipe."""
        # For each serve time, add it to the recipe
        for serve_time in serve_times:
            self.add_serve_time(serve_time)
    
    @property
    def ingredients(self) -> dict[str, IngredientQuantity]:
        """Get the ingredients for the recipe."""
        return self._ingredients
    
    @ingredients.setter
    def ingredients(self, ingredients: dict[str, IngredientQuantity]) -> None:
        """Set the ingredients for the recipe."""
        # For each ingredient, add it to the recipe
        for ingredient in ingredients.values():
            self.add_ingredient(ingredient)
    
    @property
    def recipe_types(self) -> list[str]:
        """Get the recipe types for the recipe."""
        return self._recipe_types
    
    @recipe_types.setter
    def recipe_types(self, recipe_types: list[str]) -> None:
        """Set the recipe types for the recipe."""
        # For each recipe type, add it to the recipe
        for recipe_type in recipe_types:
            self.add_recipe_type(recipe_type)

    def add_serve_time(self, serve_time: tuple[datetime, datetime]) -> None:
        """Add a serve time to the recipe."""
        # Check if the serve time is already in the recipe
        if serve_time in self._serve_times:
            return None
        # Add the serve time to the recipe
        self._serve_times.append(serve_time)

    def remove_serve_time(self, serve_time: tuple[datetime, datetime]) -> None:
        """Remove a serve time from the recipe."""
        # Remove the serve time from the recipe
        self._serve_times.remove(serve_time)

    def add_ingredient(self, ingredient_quantity: IngredientQuantity) -> None:
        """Add an ingredient to the recipe."""
        # If it is already there, return None
        if ingredient_quantity.ingredient.name in self._ingredients:
            return None
        # If the ingredient has no name, raise an exception
        if ingredient_quantity.ingredient.name is None:
            raise ValueError("Cannot add unamed ingredient")
        # Otherwise, add it
        self._ingredients[ingredient_quantity.ingredient.name] = ingredient_quantity

    def remove_ingredient(self, ingredient_id: int) -> None:
        """Remove an ingredient from the recipe."""
        # Cycle through each ingredient
        for ingredient_name, ingredient_qty in self._ingredients.items():
            # Check if the ingredient ID matches the ingredient ID to remove
            if ingredient_qty.ingredient.id == ingredient_id:
                # Remove the ingredient from the recipe
                del self._ingredients[ingredient_name]
                return None
        # Raise a value error if the ingredient is not in the recipe
        raise ValueError("Ingredient not in recipe")
    
    def add_recipe_type(self, recipe_type: str) -> None:
        """Add a recipe type to the recipe."""
        # Check if the recipe type is already in the recipe
        if recipe_type in self._recipe_types:
            return None
        # Add the recipe type to the recipe
        self._recipe_types.append(recipe_type)

    def remove_recipe_type(self, recipe_type: str) -> None:
        """Remove a recipe type from the recipe."""
        # Check if the recipe type is in the recipe
        if recipe_type not in self._recipe_types:
            return None
        # Remove the recipe type from the recipe
        self._recipe_types.remove(recipe_type)