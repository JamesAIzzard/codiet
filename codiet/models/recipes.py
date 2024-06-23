from datetime import datetime

from codiet.models.ingredients import IngredientQuantity


class Recipe:
    def __init__(self, recipe_id: int, recipe_name: str):
        self.id = recipe_id
        self.name = recipe_name
        self.use_as_ingredient: bool = False
        self.description: str | None = None
        self.instructions: str | None = None
        self.reuse_as_ingredient: bool = False
        self._ingredient_quantities: dict[int, IngredientQuantity] = {}
        self._serve_time_windows: dict[int, tuple[datetime, datetime]] = {}
        self._recipe_tags: dict[int, str] = {}

    @property
    def serve_time_windows(self) -> dict[int, tuple[datetime, datetime]]:
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
    def tags(self) -> dict[int, str]:
        """Get the recipe tags for the recipe.
        Returns:
            dict[int, str]: The recipe tags for the recipe,
                where the key is the recipe tag ID and the value is the recipe tag.
        """
        return self._recipe_tags

    def add_serve_time_window(
        self, serve_time_id: int, serve_time: tuple[datetime, datetime]
    ) -> None:
        """Add a serve time to the recipe.
        Args:
            serve_time_id (int): The ID of the serve time to add.
            serve_time (tuple[datetime, datetime]): The serve time to add.
        """
        # Check if the serve time is already in the recipe
        if serve_time in self._serve_time_windows:
            return None
        # Raise a KeyError if the ID is already in the recipe
        if serve_time_id in self._serve_time_windows:
            raise KeyError("Serve time ID already in recipe")
        # Add the serve time to the recipe
        self._serve_time_windows[serve_time_id] = serve_time

    def update_serve_time_window(
        self, serve_time_id: int, serve_time: tuple[datetime, datetime]
    ) -> None:
        """Update a serve time in the recipe.
        Args:
            serve_time_id (int): The ID of the serve time to update.
            serve_time (tuple[datetime, datetime]): The serve time to update.
        """
        # Check the id is in the recipe
        if serve_time_id not in self._serve_time_windows:
            raise KeyError("Serve time ID not in recipe")
        # Update the serve time in the recipe
        self._serve_time_windows[serve_time_id] = serve_time

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

    def add_recipe_tag(self, tag_id: int, tag: str) -> None:
        """Add a recipe tag to the recipe.
        Args:
            tag_id (int): The ID of the recipe tag to add, unique to this specific
                instance of the tag on this recipe.
            tag (str): The recipe tag to add.
        """
        # Check if the recipe tag is already in the recipe
        if tag in self._recipe_tags.values():
            return None
        # Raise an exception if the ID is already in the recipe
        if tag_id in self._recipe_tags:
            raise KeyError("Recipe tag ID already in recipe")
        # Add the recipe tag to the recipe
        self._recipe_tags[tag_id] = tag

    def remove_recipe_tag(self, tag: str) -> None:
        """Remove a recipe tag from the recipe."""
        # Check if the recipe tag is in the recipe
        if tag not in self._recipe_tags:
            return None
        # Remove the recipe tag from the recipe
        self._recipe_tags.remove(tag)
