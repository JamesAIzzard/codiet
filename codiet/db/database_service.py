from typing import Any

from PyQt6.QtCore import QObject, pyqtSignal

from codiet.utils.map import Map
from codiet.db.repository import Repository
from codiet.db.ingredient_db_service import IngredientDBService
from codiet.db.unit_db_service import UnitDBService
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
from codiet.models.nutrients import Nutrient
from codiet.models.ingredients.ingredient import Ingredient
from codiet.models.ingredients.ingredient_quantity import IngredientQuantity
from codiet.models.nutrients.entity_nutrient_quantity import (
    EntityNutrientQuantity,
)
from codiet.models.time import RecipeServeTimeWindow
from codiet.models.recipes.recipe import Recipe


class DatabaseService(QObject):
    """Service for interacting with the database."""

    ingredientIDNameChanged = pyqtSignal(object)
    unitIDNameChanged = pyqtSignal(object)
    flagIDNameChanged = pyqtSignal(object)
    nutrientIDNameChanged = pyqtSignal(object)
    recipeTagIDNameChanged = pyqtSignal(object)

    def __init__(self, repository: Repository, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._repo = repository

        # Cache the gram id
        self._gram_id: int|None = None

        # Create some cached maps
        self.flag_id_name_map: Map[int, str] = Map(one_to_one=True)
        self._cache_flag_id_name_map()
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

    def create_global_flags(self, flags: list[str]) -> None:
        """Insert the global flags into the database.
        Designed to accept the list of strings defined in the
        JSON config file.
        Args:
            flags (list[str]): A list of flag names.
        """
        for flag in flags:
            self.repository.create_global_flag(flag)

        # Recache the flag id name map and emit the signal
        self._cache_flag_id_name_map()

    # FIXME: The issue with this block of code is it is trying to do more than one thing.
    # It is trying to convert the JSON data into nutrients, and save the nutrients,
    # all at the same time. This is a violation of the single responsibility principle.
    def create_global_nutrients(
        self, nutrient_data: dict[str, Any], parent_id: int | None = None
    ) -> None:
        """Recursively adds nutrients and their aliases into the database.
        Designed to accept the nested dictionary structure defined in the
        JSON config file.
        Args:
            nutrient_data (dict[str, Any]): The nutrient data to insert.
            parent_id (int|None): The parent nutrient ID.
        """
        for nutrient_name, nutrient_info in nutrient_data.items():
            # Insert the nutrient
            nutrient_id = self.repository.create_global_nutrient(
                name=nutrient_name, parent_id=parent_id
            )
            # Insert the aliases for the nutrient
            for alias in nutrient_info.get("aliases", []):
                self.repository.create_nutrient_alias(
                    alias=alias, primary_nutrient_id=nutrient_id
                )
            # Recursively insert the child nutrients
            if "children" in nutrient_info:
                self.create_global_nutrients(
                    nutrient_info["children"], parent_id=nutrient_id
                )

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

    def create_ingredient_nutrient_quantity(self, ing_nutr_qty: EntityNutrientQuantity) -> EntityNutrientQuantity:
        """Creates an entry for the ingredient nutrient quantity in the database.
        Returns the object, with the id populated.

        Args:
            ing_nutr_qty (EntityNutrientQuantity): The nutrient quantity object.
        Returns:
            EntityNutrientQuantity: The created nutrient quantity object.
        """
        # Raise an exception if the parent entity ID is not set
        if ing_nutr_qty.parent_entity_id is None:
            raise ValueError("The parent entity ID must be set.")
        # Insert the nutrient quantity into the database
        nutrient_quantity_id = self.repository.create_ingredient_nutrient_quantity(
            ingredient_id=ing_nutr_qty.parent_entity_id,
            global_nutrient_id=ing_nutr_qty.nutrient_id,
            ntr_mass_qty=ing_nutr_qty.nutrient_mass_value,
            ntr_mass_unit_id=ing_nutr_qty.nutrient_mass_unit_id,
            ing_grams_qty=ing_nutr_qty.entity_grams_value,
        )
        # Populate the ID and return the object
        ing_nutr_qty.id = nutrient_quantity_id
        return ing_nutr_qty

    def create_empty_recipe(self, recipe_name: str) -> Recipe:
        """Creates an empty recipe with the given name."""
        # Insert the recipe name into the database
        recipe_id = self.repository.create_recipe_name(recipe_name)
        # Init the recipe
        recipe = Recipe(
            recipe_name=recipe_name,
            recipe_id=recipe_id,
        )
        # Return the recipe
        return recipe

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

    def read_all_global_nutrients(self) -> dict[int, Nutrient]:
        """Returns all the global nutrients.
        Returns:
            Dict[int, Nutrient]: A dictionary of global nutrients, where the key is the
            id of each specific nutrient.
        """
        # Fetch the data for all the nutrients
        all_nutrients_data = self.repository.read_all_global_nutrients()
        
        # Init a dict to hold the nutrients and a dict to hold child relationships
        nutrients = {}
        children = {}
        
        # Cycle through the raw data to create nutrients and record child relationships
        for nutrient_id, nutrient_data in all_nutrients_data.items():
            nutrient = Nutrient(
                id=nutrient_id,
                nutrient_name=nutrient_data["nutrient_name"],
                aliases=nutrient_data["aliases"],
                parent_id=nutrient_data["parent_id"],
            )
            nutrients[nutrient_id] = nutrient
            if nutrient.parent_id is not None:
                if nutrient.parent_id not in children:
                    children[nutrient.parent_id] = []
                children[nutrient.parent_id].append(nutrient_id)
        
        # Populate the child_ids for each nutrient
        for nutrient_id, nutrient in nutrients.items():
            nutrient.child_ids = children.get(nutrient_id, [])
        
        return nutrients

    def read_ingredient_nutrient_quantities(
        self, ingredient_id: int
    ) -> dict[int, EntityNutrientQuantity]:
        """Returns the nutrient quantities for the given ingredient.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            dict[int, IngredientNutrientQuantity]: A dictionary of nutrient quantities, where the key is the
            id of each specific nutrient quantity.
        """
        # Init a dict to hold the nutrient quantities
        nutrient_quantities: dict[int, EntityNutrientQuantity] = {}
        # Fetch the raw data from the repo
        raw_nutrient_quantities = self._repo.read_ingredient_nutrient_quantities(
            ingredient_id
        )
        # Cycle through the raw data
        for nutrient_id, nutrient_qty_data in raw_nutrient_quantities.items():
            # And add the data to the dict
            nutrient_quantities[nutrient_id] = EntityNutrientQuantity(
                id=nutrient_qty_data["id"],
                nutrient_id=nutrient_id,
                entity_id=ingredient_id,
                ntr_mass_value=nutrient_qty_data["ntr_mass_value"],
                ntr_mass_unit_id=nutrient_qty_data["ntr_mass_unit_id"],
                entity_grams_qty=nutrient_qty_data["ing_grams_value"],
            )
        return nutrient_quantities

    def read_recipe(self, recipe_id: int) -> Recipe:
        """Returns the name of the recipe with the given ID."""
        raise NotImplementedError

    def update_ingredient_nutrient_quantity(self, ing_nutr_qty: EntityNutrientQuantity) -> None:
        """Updates the nutrient quantity in the database.
        Args:
            ing_nutr_qty (EntityNutrientQuantity): The nutrient quantity object.
        """
        # Raise an exception if the parent entity ID is not set
        if ing_nutr_qty.parent_entity_id is None:
            raise ValueError("The parent entity ID must be set.")
        # Update the nutrient quantity in the database
        self.repository.update_ingredient_nutrient_quantity(
            ingredient_id=ing_nutr_qty.parent_entity_id,
            global_nutrient_id=ing_nutr_qty.nutrient_id,
            ntr_mass_qty=ing_nutr_qty.nutrient_mass_value,
            ntr_mass_unit_id=ing_nutr_qty.nutrient_mass_unit_id,
            ing_grams_qty=ing_nutr_qty.entity_grams_value,
        )

    def _cache_flag_id_name_map(self) -> None:
        """Re(generates) the cached flag ID to name map
        Emits the signal for the flag ID to name map change.

        Returns:
            Map: A map associating flag ID's with names.
        """
        # Fetch all the flags
        flags = self.repository.read_all_global_flags()
        # Clear the map
        self.flag_id_name_map.clear()
        # Add each flag to the map
        for flag_id, flag_name in flags.items():
            self.flag_id_name_map.add_mapping(key=flag_id, value=flag_name)
        # Emit the signal
        self.flagIDNameChanged.emit(self.flag_id_name_map)

    def _cache_nutrient_id_name_map(self) -> None:
        """Re(generates) the cached nutrient ID to name map
        Emits the signal for the nutrient ID to name map change.

        Returns:
            Map: A map associating nutrient ID's with names.
        """
        # Fetch all the nutrients
        nutrients = self.repository.read_all_global_nutrients()
        # Clear the map
        self.nutrient_id_name_map.clear()
        # Add each nutrient to the map
        for nutrient_id, nutrient_data in nutrients.items():
            self.nutrient_id_name_map.add_mapping(key=nutrient_id, value=nutrient_data["nutrient_name"])
        # Emit the signal
        self.nutrientIDNameChanged.emit(self.nutrient_id_name_map)

    def _cache_recipe_tag_id_name_map(self) -> None:
        """Re(generates) the cached recipe tag ID to name map
        Emits the signal for the recipe tag ID to name map change.

        Returns:
            Map: A map associating recipe tag ID's with names.
        """
        # Fetch all the recipe tags
        recipe_tags = self.repository.read_all_global_recipe_tags()
        # Clear the map
        self.recipe_tag_id_name_map.clear()
        # Add each recipe tag to the map
        for tag_id, tag_name in recipe_tags.items():
            self.recipe_tag_id_name_map.add_mapping(key=tag_id, value=tag_name)
        # Emit the signal
        self.recipeTagIDNameChanged.emit(self.recipe_tag_id_name_map)