from typing import Collection

from PyQt6.QtCore import pyqtSignal

from codiet.db.database_service.database_service_base import DatabaseServiceBase
from codiet.utils import Map, IUC
from codiet.model.ingredients.ingredient import Ingredient
from codiet.model.nutrients.nutrient_quantity import NutrientQuantity
from codiet.model.flags import Flag

class IngredientDBService(DatabaseServiceBase):
    """Database service module responsible for handling ingredients."""

    ingredientIDNameChanged = pyqtSignal()

    def __init__(self, *args, **kwargs):
        """Initialise the ingredient database service."""
        super().__init__(*args, **kwargs)

        # Cache the ingredient id-name map
        self._ingredient_id_name_map: Map[int, str]|None = None

    @property
    def ingredient_id_name_map(self) -> Map[int, str]:
        """Get the global ingredient id-name map."""
        if self._ingredient_id_name_map is None:
            self._cache_ingredient_name_id_map()
        return self._ingredient_id_name_map # type: ignore # checked in the property setter

    def create_ingredient(self, ingredient: Ingredient, _signal:bool=True) -> Ingredient:
        """Creates an ingredient in the database.
        Returns:
            Ingredient: The created ingredient, with the ID populated.
        """
        # Check the ingredient name is set
        if ingredient.name is None:
            raise ValueError("Ingredient name must be set.")
        
        # Check the ID is not set
        if ingredient.id is not None:
            raise ValueError("Ingredient cannot have a previously set ID.")

        # Create the ingredient base
        ingredient.id = self._repository.ingredients.create_ingredient_base(
            ingredient_name=ingredient.name,
            ingredient_description=ingredient.description,
            ingredient_gi=ingredient.gi,
            cost_value=ingredient.cost_value,
            cost_qty_unit_id=ingredient.cost_qty_unit.id,
            cost_qty_value=ingredient.cost_qty_value,
            standard_unit_id=ingredient.standard_unit.id
        )

        if _signal:
            self._cache_ingredient_name_id_map()
            self.ingredientIDNameChanged.emit()

        return ingredient

    def create_ingredients(self, ingredients: Collection[Ingredient]) -> None:
        """Creates multiple ingredients in the database."""
        for ingredient in ingredients:
            self.create_ingredient(ingredient, _signal=False)
        self._cache_ingredient_name_id_map()
        self.ingredientIDNameChanged.emit()

    def read_ingredient_from_id(self, ingredient_id: int) -> Ingredient:
        """Returns the ingredient with the given name."""

        # Read the ingredient base
        ingredient_base_data = self._repository.ingredients.read_ingredient_base(ingredient_id)

        # Init a fresh ingredient instance
        ingredient = Ingredient(
            id=ingredient_base_data["id"],
            name=ingredient_base_data["name"],
            description=ingredient_base_data["description"],
            gi=ingredient_base_data["gi"],
            cost_value=ingredient_base_data["cost_value"],
            cost_qty_unit_id=ingredient_base_data["cost_qty_unit_id"],
            cost_qty_value=ingredient_base_data["cost_qty_value"],
            standard_unit_id=ingredient_base_data["standard_unit_id"]
        )

        # Fetch and add the flags
        flags_data = self._repository.flags.read_ingredient_flags(ingredient_id)
        
        for ingredient_flag_id, flag_data in flags_data.items():

            # Create the flag
            flag = IngredientFlag(
                id=ingredient_flag_id,
                global_flag_id=flag_data["global_flag_id"],
                ingredient_id=ingredient_id,
                flag_name=self._db_service.flags.flag_id_name_map.get_value(flag_data["global_flag_id"]),
                flag_value=flag_data["flag_value"]
            )

            # Add the flag to the ingredient
            ingredient.add_flag(flag)

        # Fetch and add the nutrients
        nutrient_quantities_data = self._repository.nutrients.read_ingredient_nutrient_quantities(ingredient_id)

        for nutrient_quantity_id, nutrient_quantity_data in nutrient_quantities_data.items():
                
                # Create the nutrient quantity
                nutrient_quantity = NutrientQuantity(
                    id=nutrient_quantity_id,
                    nutrient=self._db_service.nutrients.get_nutrient_by_id(nutrient_quantity_data["global_nutrient_id"]),
                    ingredient=ingredient,
                    nutrient_mass_unit=self._db_service.units.get_unit_by_id(nutrient_quantity_data["ntr_mass_unit_id"]),
                    nutrient_mass_value=nutrient_quantity_data["nutrient_mass_value"],
                    ingredient_grams_value=nutrient_quantity_data["ingredient_grams_value"]
                )
    
                # Add the nutrient quantity to the ingredient
                ingredient._add_nutrient_quantity(nutrient_quantity)

        # Return the completed ingredient
        return ingredient

    def read_ingredient_from_name(self, ingredient_name: str) -> Ingredient:
        """Returns the ingredient with the given name."""
        # Get the ID of the ingredient
        ingredient_id = self.ingredient_id_name_map.get_key(ingredient_name)
        return self.read_ingredient_from_id(ingredient_id)

    def read_ingredient_flags(self, ingredient_id: int) -> IUC[Flag]:
        """Returns the flags for the ingredient."""
        return self._repository.ingredients.read_ingredient_flags(ingredient_id)

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
            ingredient.standard_unit_id = self._db_service.units.gram_id
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
            ingredient.cost_qty_unit_id = self._db_service.units.gram_id

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
        """Re(generates) the cached ingredient ID to name map.
        We clear the map instead of recreating so we don't break any references.
        """
        # If the map does not exist yet, create it
        if self._ingredient_id_name_map is None:
            self._ingredient_id_name_map = Map[int, str](one_to_one=True)

        # Fetch all the ingredients
        ingredients = self._repository.ingredients.read_all_ingredient_names()

        # Clear the existing map
        self._ingredient_id_name_map.clear()

        # Add each ingredient to the map
        for ingredient_id, ingredient_name in ingredients.items():
            self._ingredient_id_name_map.add_mapping(key=ingredient_id, value=ingredient_name)          