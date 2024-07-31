from typing import TYPE_CHECKING

from PyQt6.QtCore import QObject, pyqtSignal

if TYPE_CHECKING:
    from .database_service import DatabaseService
from .repository import Repository
from codiet.utils.map import Map
from codiet.models.ingredients.ingredient import Ingredient

class IngredientDBService(QObject):
    """Database service module responsible for handling ingredients."""

    ingredientIDNameChanged = pyqtSignal(object)

    def __init__(self, db_service:'DatabaseService', repository:Repository):
        """Initialise the ingredient database service."""
        super().__init__()

        self._db_service = db_service
        self._repository = repository

        # Cache the ingredient id-name map
        self.ingredient_id_name_map: Map[int, str] = Map(one_to_one=True)
        self._cache_ingredient_name_id_map()

    def create_ingredient(self, ingredient: Ingredient) -> Ingredient:
        """Creates an ingredient in the database.
        Args:
            ingredient (Ingredient): The ingredient to create.
        Returns:
            Ingredient: The created ingredient.
        """
        # Insert the ingredient name into the database
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        ingredient.id = self._repository.create_ingredient_name(ingredient.name)

        # Recache the ingredient name id map and emit the signal
        self._cache_ingredient_name_id_map()

        # Now we have an id, we can use the update method
        self.update_ingredient(ingredient)

        return ingredient

    def read_ingredient(self, ingredient_id: int) -> Ingredient:
        """Returns the ingredient with the given name.
        Args:
            ingredient_id (int): The id of the ingredient.
        Returns:
            Ingredient: The ingredient with the given id.
        """


        # Fetch the ingredient name corresponding to the id
        ingredient_name = self._repository.read_ingredient_name(ingredient_id)

        # Init a fresh ingredient instance
        ingredient = Ingredient(
            id=ingredient_id,
            name=ingredient_name
        )

        # Fetch the description
        ingredient.description = self._repository.read_ingredient_description(
            ingredient_id
        )

        # Fetch the ingredient standard id
        standard_unit_id = self._repository.read_ingredient_standard_unit_id(
            ingredient_id
        )
        ingredient.standard_unit_id = standard_unit_id

        # Fetch the cost data
        cost_data = self._repository.read_ingredient_cost(ingredient_id)
        # If the cost qty unit id is not set, set it to the standard unit id
        if cost_data["cost_qty_unit_id"] is None:
            cost_data["cost_qty_unit_id"] = standard_unit_id
        # Populate the cost data
        ingredient.cost_value = cost_data["cost_value"]
        ingredient.cost_qty_unit_id = cost_data["cost_qty_unit_id"]
        ingredient.cost_qty_value = cost_data["cost_qty_value"]

        # Fetch the unit conversions
        unit_conversions = self._db_service.read_ingredient_unit_conversions(
            ingredient_id=ingredient_id
        )
        for _, conversion in unit_conversions.items():
            ingredient.add_unit_conversion(conversion)

        # Fetch the flags
        flags = self._repository.read_ingredient_flags(ingredient_id)
        for flag_id, flag_value in flags.items():
            ingredient.add_flag(flag_id, flag_value)

        # Fetch the GI
        ingredient.gi = self._repository.read_ingredient_gi(ingredient_id)

        # Fetch the nutrients
        nutrient_quantities = self._db_service.read_ingredient_nutrient_quantities(
            ingredient_id=ingredient_id
        )
        for _, nutrient_quantity in nutrient_quantities.items():
            ingredient.add_nutrient_quantity(nutrient_quantity)

        # Return the completed ingredient
        return ingredient

    def update_ingredient_name(self, ingredient_id: int, new_name: str) -> None:
        """Updates the name of the ingredient in the database.
        Args:
            ingredient_id (int): The id of the ingredient.
            new_name (str): The new name of the ingredient.
        """
        # Grab the old name
        old_name = self.ingredient_id_name_map.get_value(ingredient_id)

        # Update the name in the database
        self._repository.update_ingredient_name(ingredient_id, new_name)

        # If the name has changed, recache
        if old_name != new_name:
            self._cache_ingredient_name_id_map()

    def update_ingredient(self, ingredient: Ingredient) -> None:
        """Updates the ingredient in the database."""
        # To use update, id must be set
        if ingredient.id is None:
            raise ValueError("Ingredient ID must be set.")
        
        # Update the name
        self.update_ingredient_name(ingredient.id, ingredient.name) # type: ignore
        
        # Update the description
        self._repository.update_ingredient_description(
            ingredient.id, ingredient.description
        )
        
        # Update the standard unit
        # If the standard unit is not set, set it to the gram unit
        if ingredient.standard_unit_id is None:
            ingredient.standard_unit_id = self._db_service.gram_id
        self._repository.update_ingredient_standard_unit_id(
            ingredient.id, ingredient.standard_unit_id
        )
       
        # Update the unit conversions
        # Read the existing saved unit conversions
        existing_unit_conversions = self._repository.read_ingredient_unit_conversions(
            ingredient.id
        )
        # Compare the existing unit conversions with the new ones
        for unit_conversion in ingredient.unit_conversions.values():
            # If the unit conversion is new, add it
            if unit_conversion.id not in existing_unit_conversions:
                self._repository.create_ingredient_unit_conversion(
                    ingredient_id=ingredient.id,
                    from_unit_id=unit_conversion.from_unit_id,
                    from_unit_qty=unit_conversion.from_unit_qty,
                    to_unit_id=unit_conversion.to_unit_id,
                    to_unit_qty=unit_conversion.to_unit_qty,
                )
            # If the unit conversion is already saved, update it
            else:
                self._repository.update_ingredient_unit_conversion(
                    ingredient_unit_id=unit_conversion.id,
                    from_unit_id=unit_conversion.from_unit_id,
                    from_unit_qty=unit_conversion.from_unit_qty,
                    to_unit_id=unit_conversion.to_unit_id,
                    to_unit_qty=unit_conversion.to_unit_qty,
                )
        # Delete any unit conversions that are no longer needed
        for unit_conversion_id in existing_unit_conversions.keys():
            if unit_conversion_id not in ingredient.unit_conversions:
                self._repository.delete_ingredient_unit_conversion(unit_conversion_id)      
        
        # Update the cost data
        # If the cost_qty_unit_id is not set, set it to the standard unit
        if ingredient.cost_qty_unit_id is None:
            ingredient.cost_qty_unit_id = self._db_service.gram_id

        self._repository.update_ingredient_cost(
            ingredient_id=ingredient.id,
            cost_value=ingredient.cost_value,
            cost_qty_unit_id=ingredient.cost_qty_unit_id,
            cost_qty_value=ingredient.cost_qty_value,
        )

        # Update the flags
        # Read the existing saved flags
        existing_flags = self._repository.read_ingredient_flags(ingredient.id)
        # Compare the existing flags with the new ones
        for flag_id, flag_value in ingredient.flags.items():
            # If the flag is new, add it
            if flag_id not in existing_flags:
                self._repository.create_ingredient_flag(
                    ingredient_id=ingredient.id,
                    flag_id=flag_id,
                    flag_value=flag_value,
                )
            # If the flag is already saved, update it
            else:
                self._repository.update_ingredient_flag(
                    ingredient_id=ingredient.id,
                    flag_id=flag_id,
                    flag_value=flag_value,
                )
        # Delete any flags that are no longer needed
        for flag_id in existing_flags.keys():
            if flag_id not in ingredient.flags:
                self._repository.delete_ingredient_flag(ingredient.id, flag_id)
        
        # Update the GI
        self._repository.update_ingredient_gi(ingredient.id, ingredient.gi)
        
        # Update the nutrient quantities
        # First, read the existing saved nutrient quantities
        existing_nutrient_quantities = self._repository.read_ingredient_nutrient_quantities(
            ingredient.id
        )
        # Compare the existing nutrient quantities with the new ones
        for nutrient_quantity in ingredient.nutrient_quantities.values():
            # If the nutrient quantity is new, add it
            if nutrient_quantity.id not in existing_nutrient_quantities:
                self._repository.create_ingredient_nutrient_quantity(
                    ingredient_id=ingredient.id,
                    global_nutrient_id=nutrient_quantity.nutrient_id,
                    ntr_mass_qty=nutrient_quantity.nutrient_mass_value,
                    ntr_mass_unit_id=nutrient_quantity.nutrient_mass_unit_id,
                    ing_grams_qty=nutrient_quantity.entity_grams_value,
                )
            # If the nutrient quantity is already saved, update it
            else:
                self._repository.update_ingredient_nutrient_quantity(
                    ingredient_id=ingredient.id,
                    global_nutrient_id=nutrient_quantity.nutrient_id,
                    ntr_mass_qty=nutrient_quantity.nutrient_mass_value,
                    ntr_mass_unit_id=nutrient_quantity.nutrient_mass_unit_id,
                    ing_grams_qty=nutrient_quantity.entity_grams_value,
                )
        # Delete any nutrient quantities that are no longer needed
        for nutrient_quantity_id in existing_nutrient_quantities.keys():
            if nutrient_quantity_id not in ingredient.nutrient_quantities:
                self._repository.delete_ingredient_nutrient_quantity(
                    ingredient_id=ingredient.id, global_nutrient_id=nutrient_quantity_id
                )

    def delete_ingredient(self, ingredient_id: int) -> None:
        """Deletes the ingredient with the given ID.
        Args:
            ingredient_id (int): The id of the ingredient.
        """
        self._repository.delete_ingredient(ingredient_id)

        # Recache the ingredient name id map
        self._cache_ingredient_name_id_map()

    def _cache_ingredient_name_id_map(self) -> None:
        """Re(generates) the cached ingredient ID to name map
        Emits the signal for the ingredient ID to name map change.

        Returns:
            Map: A map associating ingredient ID's with names.
        """
        # Fetch all the ingredients
        ingredients = self._repository.read_all_ingredient_names()

        # Clear the map
        self.ingredient_id_name_map.clear()

        # Add each ingredient to the map
        for ingredient_id, ingredient_name in ingredients.items():
            self.ingredient_id_name_map.add_mapping(key=ingredient_id, value=ingredient_name)

        # Emit the signal
        self.ingredientIDNameChanged.emit(self.ingredient_id_name_map)            