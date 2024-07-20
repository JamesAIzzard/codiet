from datetime import datetime

from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.time import RecipeServeTimeWindow

class Recipe:
    def __init__(self, recipe_id: int, recipe_name: str):
        self.id = recipe_id
        self.name = recipe_name
        self.use_as_ingredient: bool = False
        self.description: str | None = None
        self.instructions: str | None = None
        self.reuse_as_ingredient: bool = False
        self._ingredient_quantities: dict[int, IngredientQuantity] = {}
        self._serve_time_windows: dict[int, RecipeServeTimeWindow] = {}
        self._recipe_tags: list[int] = []

    @property
    def serve_time_windows(self) -> dict[int, RecipeServeTimeWindow]:
        """Get the serve times for the recipe.
        Returns:
            dict[int, tuple[datetime, datetime]]: The serve times for the recipe,
                where the key is the serve time ID and the value is the serve time.
        """
        return self._serve_time_windows

    @property
    def ingredient_quantities(self) -> dict[int, IngredientQuantity]:
        """Get the ingredients for the recipe.
        Returns:
            dict[int, IngredientQuantity]: The ingredients for the recipe,
                where the key is the ingredient ID and the value is the ingredient quantity.
        """
        return self._ingredient_quantities

    @property
    def tags(self) -> list[int]:
        """Get the recipe tags for the recipe.
        Returns:
            dict[int, str]: The recipe tags for the recipe,
                where the key is the recipe tag ID and the value is the recipe tag.
        """
        return self._recipe_tags

    def add_serve_time_window(self, serve_time_window:RecipeServeTimeWindow) -> None:
        """Add a serve time to the recipe.
        Args:
            serve_time_window (RecipeServeTimeWindow): The serve time to add.
        """
        # Raise an exception if the serve time ID is already in the recipe
        if serve_time_window.id in self._serve_time_windows:
            raise KeyError("Serve time ID already in recipe")
        # Raise an exception if the serve time is already in the recipe
        for serve_time in self._serve_time_windows.values():
            if serve_time.window_string == serve_time_window.window_string:
                raise KeyError("Serve time already in recipe")
        self._serve_time_windows[serve_time_window.id] = serve_time_window

    def update_serve_time_window(self, serve_time_window: RecipeServeTimeWindow) -> None:
        """Update a serve time in the recipe.
        Args:
            serve_time_window (RecipeServeTimeWindow): The serve time to update.
        """
        # Check the serve time is in the recipe
        if serve_time_window.id not in self._serve_time_windows:
            raise KeyError("Serve time ID not in recipe")
        # Update the serve time in the recipe
        self._serve_time_windows[serve_time_window.id] = serve_time_window

    def remove_serve_time_window(self, serve_time_id: int) -> None:
        """Remove a serve time from the recipe.
        Args:
            serve_time_id (int): The ID of the serve time to remove.
        """
        # Remove the serve time from the recipe
        del self._serve_time_windows[serve_time_id]

    def add_ingredient_quantity(self, ingredient_quantity: IngredientQuantity) -> None:
        """Add an ingredient to the recipe."""
        # Raise an exception if the ingredient quantity ID is already in the recipe
        if ingredient_quantity.id in self._ingredient_quantities:
            raise KeyError("Ingredient quantity ID already in recipe")
        # Raise an exception if an ingredient quantity with the same ingredient
        # is already in the recipe
        for ingredient_qty in self._ingredient_quantities.values():
            if ingredient_qty.ingredient_id == ingredient_quantity.ingredient_id:
                raise KeyError("Ingredient already in recipe")
        # Go ahead and add it
        self._ingredient_quantities[ingredient_quantity.id] = ingredient_quantity

    def update_ingredient_quantity(
        self, ingredient_quantity: IngredientQuantity
    ) -> None:
        """Update an ingredient in the recipe."""
        # Check the ingredient quantity is in the recipe
        if ingredient_quantity.id not in self._ingredient_quantities:
            raise KeyError("Ingredient quantity ID not in recipe")
        # Update the ingredient quantity in the recipe
        self._ingredient_quantities[ingredient_quantity.id] = ingredient_quantity

    def remove_ingredient_quantity(self, ingredient_quantity_id: int) -> None:
        """Remove an ingredient from the recipe."""
        # Remove the ingredient from the recipe
        del self._ingredient_quantities[ingredient_quantity_id]

    def add_recipe_tag(self, tag_id: int) -> None:
        """Add a recipe tag to the recipe.
        Args:
            tag_id (int): The ID of the recipe tag to add, unique to this specific
                instance of the tag on this recipe.
        """
        # Raise an exception if the recipe tag is already in the recipe
        if tag_id in self._recipe_tags:
            raise KeyError("Recipe tag already in recipe")
        # Add the recipe tag to the recipe
        self._recipe_tags.append(tag_id)

    def remove_recipe_tag(self, tag_id: int) -> None:
        """Remove a recipe tag from the recipe.
        Args:
            tag_id (int): The ID of the recipe tag to remove.
        """
        # Remove the recipe tag from the recipe
        self._recipe_tags.remove(tag_id)
