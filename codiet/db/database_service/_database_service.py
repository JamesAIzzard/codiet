from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from codiet.utils.map import Map
from codiet.db.repository import Repository
from codiet.db.database_service.ingredient_db_service import IngredientDBService
from codiet.db.database_service.unit_db_service import UnitDBService
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.models.nutrients import Nutrient
from codiet.models.ingredients.ingredient import Ingredient
from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.nutrients.ingredient_nutrient_quantity import (
    IngredientNutrientQuantity,
)
from codiet.models.time.recipe_serve_time_window import RecipeServeTimeWindow
from codiet.models.recipes.recipe import Recipe


class DatabaseService(QObject):
    """Service for interacting with the database."""

    ingredientIDNameChanged = pyqtSignal(object)
    unitIDNameChanged = pyqtSignal(object)
    nutrientIDNameChanged = pyqtSignal(object)
    recipeTagIDNameChanged = pyqtSignal(object)

    def __init__(self, repository: Repository, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._repo = repository

        # Cache the gram id
        self._gram_id: int|None = None

        # Create some cached maps
        self.nutrient_id_name_map: Map[int, str] = Map(one_to_one=True)
        self._cache_nutrient_id_name_map()
        self.recipe_tag_id_name_map: Map[int, str] = Map(one_to_one=True)
        self._cache_recipe_tag_id_name_map()

        # Initialise sub-services
        self.ingredients = IngredientDBService(db_service=self, repository=self._repo)
        self.units = UnitDBService(db_service=self, repository=self._repo)

    @property
    def repository(self) -> Repository:
        return self._repo


    # FIXME: As above, this should accept a list of tag objects. Converting the 
    # JSON data into tag objects should be done elsewhere.
    def create_global_recipe_tags(self, tag_data: dict[str, dict]) -> None:
        """Insert the global recipe tags into the database.
        Works through the tree structure provided in tag data and inserts
        the tags into the database.
        Args:
            tag_data (dict[str, dict]): The recipe tag data from the
                JSON config file.
        Returns:
            None
        """

        def insert_tags(data: dict[str, dict], parent_id: int | None = None) -> None:
            for tag_name, children in data.items():
                # Insert the current tag and get its ID
                tag_id = self.repository.create_global_recipe_tag(tag_name, parent_id)
                # Recursively insert children tags
                if children:
                    insert_tags(children, tag_id)

        # Start the recursive insertion with the root tags
        insert_tags(tag_data)

    def create_recipe_serve_time_window(
        self, recipe_id: int, window_string: str
    ) -> RecipeServeTimeWindow:
        """Creates a serve time window for the given recipe.
        Args:
            recipe_id (int): The id of the recipe.
            window_string (str): The string representing the time window.
        Returns:
            RecipeServeTimeWindow: The created serve time window.
        """
        # Insert the serve time window into the database
        id = self.repository.create_recipe_serve_time_window(recipe_id, window_string)
        # Init the serve time window
        serve_time_window = RecipeServeTimeWindow(
            id=id, recipe_id=recipe_id, window_string=window_string
        )
        return serve_time_window

    def create_recipe_ingredient_quantity(
        self,
        recipe_id: int,
        ingredient_id: int,
        qty_unit_id: int | None,
        qty_value: float | None,
        qty_ltol: float | None,
        qty_utol: float | None,
    ) -> IngredientQuantity:
        """Creates an ingredient quantity for the given recipe.
        Args:
            recipe_id (int): The id of the recipe.
            ingredient_id (int): The id of the ingredient.
            qty_unit_id (int|None): The unit id of the quantity.
            qty_value (float|None): The value of the quantity.
            qty_ltol (float|None): The lower tolerance of the quantity.
            qty_utol (float|None): The upper tolerance of the quantity.
        Returns:
            IngredientQuantity: The created ingredient quantity.
        """
        # Insert the ingredient quantity into the database
        id = self.repository.create_recipe_ingredient_quantity(
            recipe_id=recipe_id,
            ingredient_id=ingredient_id,
            qty_unit_id=qty_unit_id,
            qty_value=qty_value,
            qty_ltol=qty_ltol,
            qty_utol=qty_utol,
        )
        # Init the ingredient quantity
        ingredient_quantity = IngredientQuantity(
            id=id,
            ingredient_id=ingredient_id,
            recipe_id=recipe_id,
            qty_unit_id=qty_unit_id,
            qty_value=qty_value,
            qty_ltol=qty_ltol,
            qty_utol=qty_utol,
        )
        return ingredient_quantity
