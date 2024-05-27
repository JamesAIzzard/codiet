from datetime import datetime

from codiet.models.ingredients import IngredientQuantity

class Recipe:
    def __init__(self):
        self.name: str | None = None
        self.id: int | None = None
        self.description: str | None = None
        self.instructions: str | None = None
        self._ingredient_quantities: dict[int, IngredientQuantity] = {}
        self._serve_times: list[tuple[datetime, datetime]] = []
        self._recipe_tags: list[str] = []

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
    def ingredient_quantities(self) -> dict[int, IngredientQuantity]:
        """Get the ingredients for the recipe."""
        return self._ingredient_quantities
    
    @ingredient_quantities.setter
    def ingredient_quantities(self, ingredients: dict[int, IngredientQuantity]) -> None:
        """Set the ingredients for the recipe."""
        # For each ingredient, add it to the recipe
        for ingredient in ingredients.values():
            self.add_ingredient_quantity(ingredient)
    
    @property
    def tags(self) -> list[str]:
        """Get the recipe tags for the recipe."""
        return self._recipe_tags
    
    @tags.setter
    def tags(self, tags: list[str]) -> None:
        """Set the recipe tags for the recipe."""
        # For each recipe tag, add it to the recipe
        for recipe_tag in tags:
            self.add_recipe_tag(recipe_tag)

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

    def add_ingredient_quantity(self, ingredient_quantity: IngredientQuantity) -> None:
        """Add an ingredient to the recipe."""
        # If it is already there, return None
        if ingredient_quantity.ingredient.name in self._ingredient_quantities:
            return None
        # Raise an exception if the ID is not populated
        if ingredient_quantity.ingredient.id is None:
            raise ValueError("Ingredient ID not populated")
        # Go ahead and add it
        self._ingredient_quantities[ingredient_quantity.ingredient.id] = ingredient_quantity

    def remove_ingredient_quantity(self, ingredient_id: int) -> None:
        """Remove an ingredient from the recipe."""
        # Cycle through each ingredient
        for ingredient_name, ingredient_qty in self._ingredient_quantities.items():
            # Check if the ingredient ID matches the ingredient ID to remove
            if ingredient_qty.ingredient.id == ingredient_id:
                # Remove the ingredient from the recipe
                del self._ingredient_quantities[ingredient_name]
                return None
        # Raise a value error if the ingredient is not in the recipe
        raise ValueError("Ingredient not in recipe")
    
    def get_ingredient_quantity(self, ingredient_id: int) -> IngredientQuantity:
        """Get the quantity of an ingredient in the recipe."""
        # First, find the ingredient quantity instance associated with the id
        for ingredient_quantity in self._ingredient_quantities.values():
            # Check if the ingredient ID matches the ingredient ID to get
            if ingredient_quantity.ingredient.id == ingredient_id:
                return ingredient_quantity
        # Raise a value error if the ingredient is not in the recipe
        raise ValueError("Ingredient quantity not found.")

    def update_ingredient_quantity_value(self, ingredient_id:int, ingredient_qty_value:float|None) -> None:
        """Update the quantity of an ingredient in the recipe."""
        # Fetch the ingredient quantity
        ingredient_quantity = self.get_ingredient_quantity(ingredient_id)
        # Update the quantity value
        ingredient_quantity.qty_value = ingredient_qty_value

    def update_ingredient_quantity_unit(self, ingredient_id:int, ingredient_qty_unit:str) -> None:
        """Update the unit of an ingredient in the recipe."""
        # Fetch the ingredient quantity
        ingredient_quantity = self.get_ingredient_quantity(ingredient_id)
        # Update the quantity unit
        ingredient_quantity.qty_unit = ingredient_qty_unit

    def update_ingredient_quantity_utol(self, ingredient_id:int, ingredient_qty_utol:float|None) -> None:
        """Update the upper tolerance of an ingredient in the recipe."""
        # Fetch the ingredient quantity
        ingredient_quantity = self.get_ingredient_quantity(ingredient_id)
        # Update the quantity upper tolerance
        ingredient_quantity.upper_tol = ingredient_qty_utol
    
    def update_ingredient_quantity_ltol(self, ingredient_id:int, ingredient_qty_ltol:float|None) -> None:
        """Update the lower tolerance of an ingredient in the recipe."""
        # Fetch the ingredient quantity
        ingredient_quantity = self.get_ingredient_quantity(ingredient_id)
        # Update the quantity lower tolerance
        ingredient_quantity.lower_tol = ingredient_qty_ltol

    def add_recipe_tag(self, tag: str) -> None:
        """Add a recipe tag to the recipe."""
        # Check if the recipe tag is already in the recipe
        if tag in self._recipe_tags:
            return None
        # Add the recipe tag to the recipe
        self._recipe_tags.append(tag)

    def remove_recipe_tag(self, tag: str) -> None:
        """Remove a recipe tag from the recipe."""
        # Check if the recipe tag is in the recipe
        if tag not in self._recipe_tags:
            return None
        # Remove the recipe tag from the recipe
        self._recipe_tags.remove(tag)