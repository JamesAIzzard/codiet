from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from . import DatabaseService
from codiet.db.repository import Repository
from codiet.utils.map import Map
from codiet.models.recipes.recipe import Recipe

class RecipeDBService(QObject):
    """Database service module for recipes."""

    recipeIDNameChanged = pyqtSignal()

    def __init__(self, repository: Repository, db_service: 'DatabaseService'):
        """Initialise the recipe database service."""
        super().__init__()

        self._repository = repository
        self._db_service = db_service

        # Cache the recipe id-name map
        self._recipe_id_name_map:Map[int, str]|None = None

    def create_recipe(self, recipe: Recipe) -> Recipe:
        """Create a recipe in the database."""
        recipe_id = self._repository.create_recipe_base(
            name=recipe._name,
            use_as_ingredient=recipe._use_as_ingredient,
            description=recipe._description,
            instructions=recipe._instructions,
        )

        # Update the recipe with its new ID
        recipe.id = recipe_id

        # Add the ingredient quantities
        for recipe_ingredient_qty_id, ingredient_quantity in recipe.ingredient_quantities.items():
            _ = self._repository.create_recipe_ingredient_quantity(
                recipe_id=recipe_id,
                ingredient_id=ingredient_quantity.ingredient_id,
                unit_id=ingredient_quantity.unit_id,
                quantity=ingredient_quantity.quantity,
            )

        # Emit the signal for the recipe name change
        self.recipeIDNameChanged.emit()

        return recipe_id

    def read_recipe(self, recipe_id: int) -> Recipe:
        """Read a recipe from the database."""
        recipe_data = self._repository.read_recipe(recipe_id=recipe_id)
        return Recipe.from_dict(recipe_data)

    def update_recipe(self, recipe: Recipe) -> None:
        """Update a recipe in the database."""
        self._repository.update_recipe(
            recipe_id=recipe.id,
            recipe_name=recipe.recipe_name,
            recipe_description=recipe.recipe_description,
            recipe_instructions=recipe.recipe_instructions,
            recipe_serve_time_window=recipe.recipe_serve_time_window,
            recipe_tags=recipe.recipe_tags,
            recipe_ingredients=recipe.recipe_ingredients,
            recipe_nutrients=recipe.recipe_nutrients,
            recipe_flags=recipe.recipe_flags,
        )

        # Emit the signal for the recipe name change
        self.recipeIDNameChanged.emit()

    def delete_recipe(self, recipe_id: int) -> None:
        """Delete a recipe from the database."""
        self._repository.delete_recipe(recipe_id=recipe_id)

        # Emit the signal for the recipe name change
        self.recipeIDNameChanged.emit()

    def _cache_recipe_id_name_map(self) -> None:
        """Cache the recipe id-name map."""
        # If the map is None, create it
        if self._recipe_id_name_map is None:
            self._recipe_id_name_map = Map(one_to_one=True)

        # Fetch all the recipe names
        recipe_id_names = self._repository.read_all_recipe_names()

        # Add the recipe names to the map
        for recipe_id, recipe_name in recipe_id_names.items():
            self._recipe_id_name_map.add_mapping(key=recipe_id, value=recipe_name)

