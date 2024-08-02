from codiet.db.stored_entity import StoredEntity
from codiet.models.units.entity_unit_conversion import EntityUnitConversion
from codiet.models.nutrients.entity_nutrient_quantity import EntityNutrientQuantity


class Ingredient(StoredEntity):
    """Ingredient model."""

    def __init__(self, name:str|None=None, *args, **kwargs):
        """Initialises the class.
        Args:
            name (str): The name of the ingredient.
        """
        super().__init__(*args, **kwargs)
    
        self.name: str|None = name
        self.description: str | None = None
        self._standard_unit_id: int|None = None
        self._unit_conversions: dict[int, EntityUnitConversion] = {}   
        self._cost_unit_id: int | None = None # One day this could represent the currency
        self._cost_value: float | None = None
        self._cost_qty_unit_id: int|None = None
        self._cost_qty_value: float | None = None
        self._flags: dict[int, bool] = {}
        self.gi: float | None = None
        self._nutrient_quantities: dict[int, EntityNutrientQuantity] = {}

    @property
    def standard_unit_id(self) -> int|None:
        """Returns the standard unit ID."""
        return self._standard_unit_id
    
    @standard_unit_id.setter
    def standard_unit_id(self, value: int) -> None:
        """Sets the standard unit ID."""
        self._standard_unit_id = value
        # If cost unit ID is not set, set it to the standard unit ID
        if self._cost_unit_id is None:
            self._cost_unit_id = value

    @property
    def unit_conversions(self) -> dict[int, EntityUnitConversion]:
        """Returns the unit conversions associated with this ingredient.
        Returns:
            dict[int, IngredientUnitConversion]: The unit conversions.
                Where the key is the UID for the unit conversion on
                the ingredient.
        """
        return self._unit_conversions

    @property
    def cost_value(self) -> float | None:
        """Returns the cost value."""
        return self._cost_value
    
    @cost_value.setter
    def cost_value(self, value: float | None) -> None:
        """Sets the cost value."""
        # Raise an exception if the value is negative
        if value is not None and value < 0:
            raise ValueError("Cost value cannot be negative.")
        self._cost_value = value

    @property
    def cost_qty_unit_id(self) -> int|None:
        """Returns the cost quantity unit ID."""
        return self._cost_qty_unit_id
    
    @cost_qty_unit_id.setter
    def cost_qty_unit_id(self, value: int) -> None:
        """Sets the cost quantity unit ID."""
        # Raise an exception if the value is negative
        if value < 0:
            raise ValueError("Cost quantity unit ID cannot be negative.")
        self._cost_qty_unit_id = value

    @property
    def cost_qty_value(self) -> float | None:
        """Returns the cost quantity value."""
        return self._cost_qty_value
    
    @cost_qty_value.setter
    def cost_qty_value(self, value: float | None) -> None:
        """Sets the cost quantity value."""
        # Raise an exception if the value is negative
        if value is not None and value < 0:
            raise ValueError("Cost quantity value cannot be negative.")
        self._cost_qty_value = value

    @property
    def flags(self) -> dict[int, bool]:
        """Returns the flags.
        Returns:
            dict[int, bool|None]: The flags.
                Where the key is the global flag ID and the value is the flag value.
        """
        return self._flags

    @property
    def nutrient_quantities(self) -> dict[int, EntityNutrientQuantity]:
        """Returns the nutrient quantities.
        Returns:
            dict[int, IngredientNutrientQuantity]: The nutrient quantities.
                Where the key is the gloabl nutrient ID."""
        return self._nutrient_quantities

    def add_unit_conversion(self, unit_conversion: EntityUnitConversion) -> None:
        """Adds a unit conversion.
        Args:
            unit_conversion (IngredientUnitConversion): The unit conversion to add.
        Returns:
            None
        """
        # Raise an exception if the unit conversion ID is already in the list
        if unit_conversion.id in self._unit_conversions:
            raise KeyError(f"Unit conversion '{unit_conversion.id}' already in list.")
        # If not found, add the unit conversion
        self._unit_conversions[unit_conversion.id] = unit_conversion

    def update_unit_conversion(self, unit_conversion: EntityUnitConversion) -> None:
        """Updates a unit conversion.
        Args:
            unit_conversion (IngredientUnitConversion): The unit conversion to update.
        Returns:
            None
        """
        # Raise an exception if the unit conversion isn't in the list
        if unit_conversion.id not in self._unit_conversions:
            raise KeyError(f"Unit conversion '{unit_conversion.id}' not in list.")
        # If found, update the unit conversion
        self._unit_conversions[unit_conversion.id] = unit_conversion

    def remove_unit_conversion(self, unit_id: int) -> None:
        """Delete a unit."""
        self._unit_conversions.pop(unit_id)

    def add_flag(self, flag_id: int, value: bool) -> None:
        """Adds a flag.
        Args:
            flag_id (int): The global flag ID.
            value (bool): The flag value.
        Returns:
            None
        """
        # Raise an exception if the flag is already in the list
        if flag_id in self._flags:
            raise KeyError(f"Flag '{flag_id}' already in list.")
        # If not found, add the flag
        self._flags[flag_id] = value

    def update_flag(self, flag_id: int, value: bool) -> None:
        """Updates a flag.
        Args:
            flag_id (int): The global flag ID.
            value (bool): The flag value.
        Returns:
            None
        """
        # Raise an exception if the flag isn't in the list
        if flag_id not in self._flags:
            raise KeyError(f"Flag '{flag_id}' not in list.")
        # If found, update the flag
        self._flags[flag_id] = value

    def remove_flag(self, flag_id: int) -> None:
        """Deletes a flag."""
        # Raise an exception if the flag isn't in the list
        if flag_id not in self._flags:
            raise KeyError(f"Flag '{flag_id}' not in list.")
        self._flags.pop(flag_id)

    def set_all_flags_true(self) -> None:
        """Sets all flags to True."""
        for flag in self.flags:
            self.update_flag(flag, True)

    def set_all_flags_false(self) -> None:
        """Sets all flags to False."""
        for flag in self.flags:
            self.update_flag(flag, False)

    def add_nutrient_quantity(
        self, ingredient_nutrient_quantity: EntityNutrientQuantity
    ) -> None:
        """Updates a nutrient quantity on the ingredient."""
        # Raise an exception if the nutrient quantity is already in the list
        for nutrient_quantity in self._nutrient_quantities.values():
            if nutrient_quantity == ingredient_nutrient_quantity:
                raise KeyError(f"Nutrient quantity '{ingredient_nutrient_quantity.nutrient_id}' already in list.")
        # Go ahead and add the nutrient quantity
        self._nutrient_quantities[ingredient_nutrient_quantity.nutrient_id] = ingredient_nutrient_quantity

    def update_nutrient_quantity(
        self, ingredient_nutrient_quantity: EntityNutrientQuantity
    ) -> None:
        """Updates a nutrient quantity on the ingredient."""
        # Raise an exception if the nutrient quantity isn't in the list
        if ingredient_nutrient_quantity.nutrient_id not in self._nutrient_quantities:
            raise KeyError(f"Nutrient quantity '{ingredient_nutrient_quantity.nutrient_id}' not in list.")
        # Go ahead and update the nutrient quantity
        self._nutrient_quantities[ingredient_nutrient_quantity.nutrient_id] = ingredient_nutrient_quantity

    def remove_nutrient_quantity(self, nutrient_id: int) -> None:
        """Deletes a nutrient quantity."""
        # Raise an exception if the nutrient quantity isn't in the list
        if nutrient_id not in self._nutrient_quantities:
            raise KeyError(f"Nutrient quantity '{nutrient_id}' not in list.")
        self._nutrient_quantities.pop(nutrient_id)
