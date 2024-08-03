from codiet.db.stored_entity import StoredEntity
from codiet.models.units.unit import Unit
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.models.flags.ingredient_flag import IngredientFlag
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity


class Ingredient(StoredEntity):
    """Ingredient model."""

    def __init__(
            self, 
            name:str,
            description:str|None=None,
            standard_unit:Unit|None=None,
            unit_conversions:set[IngredientUnitConversion]|None=None,
            cost_value:float|None=None,
            cost_qty_unit:Unit|None=None,
            cost_qty_value:float|None=None,
            flags:set[IngredientFlag]|None=None,
            gi:float|None=None,
            nutrient_quantities:set[IngredientNutrientQuantity]|None=None,
            *args, **kwargs
        ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)
    
        self._name = name
        self._description = description
        self._standard_unit = standard_unit
        self._unit_conversions = unit_conversions if unit_conversions is not None else set()
        self._cost_value = cost_value
        self._cost_qty_unit = cost_qty_unit if cost_qty_unit is not None else standard_unit
        self._cost_qty_value = cost_qty_value
        self._flags = flags if flags is not None else set()
        self._gi = gi
        self._nutrient_quantities = nutrient_quantities if nutrient_quantities is not None else set()

    @property
    def name(self) -> str:
        """Returns the name."""
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """Sets the name."""
        if not value.strip().replace(" ", ""):
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def standard_unit(self) -> Unit:
        """Returns the standard unit ID."""
        if self._standard_unit is None:
            raise ValueError("Standard unit cannot be empty.")
        return self._standard_unit
    
    @standard_unit.setter
    def standard_unit(self, value: Unit) -> None:
        """Sets the standard unit ID."""
        if value is None:
            raise ValueError("Standard unit cannot be empty.")
        self._standard_unit = value
        # If cost unit ID is not set, set it to the standard unit ID
        if self._cost_qty_unit is None:
            self._cost_qty_unit = value

    @property
    def unit_conversions(self) -> frozenset[IngredientUnitConversion]:
        """Returns the unit conversions."""
        return frozenset(self._unit_conversions)

    @unit_conversions.setter
    def unit_conversions(self, value: set[IngredientUnitConversion]) -> None:
        """Sets the unit conversions."""
        self._unit_conversions = value

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
    def cost_qty_unit(self) -> Unit:
        """Returns the cost quantity unit."""
        if self._cost_qty_unit is None:
            raise ValueError("Cost quantity unit cannot be empty.")
        return self._cost_qty_unit
    
    @cost_qty_unit.setter
    def cost_qty_unit(self, value: Unit) -> None:
        """Sets the cost quantity unit ID."""
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
    def flags(self) -> frozenset[IngredientFlag]:
        """Returns the flags."""
        return frozenset(self._flags)

    @flags.setter
    def flags(self, value: set[IngredientFlag]) -> None:
        """Sets the flags."""
        self._flags = value

    @property
    def nutrient_quantities(self) -> frozenset[IngredientNutrientQuantity]:
        """Returns the nutrient quantities."""
        return frozenset(self._nutrient_quantities)

    @nutrient_quantities.setter
    def nutrient_quantities(self, value: set[IngredientNutrientQuantity]) -> None:
        """Sets the nutrient quantities."""
        self._nutrient_quantities = value

    def update_unit_conversions(self, unit_conversions: set[IngredientUnitConversion]) -> None:
        """Updates unit conversions."""
        self._unit_conversions.difference_update(unit_conversions)
        self._unit_conversions.update(unit_conversions)

    def remove_unit_conversions(self, unit_conversions: set[IngredientUnitConversion]) -> None:
        """Delete unit conversions."""
        if not unit_conversions.issubset(self._unit_conversions):
            raise KeyError("One or more unit conversions not found in ingredient.")
        self._unit_conversions.difference_update(unit_conversions)

    def update_flags(self, flags: set[IngredientFlag]) -> None:
        """Updates the flags passed in the set."""
        self._flags.difference_update(flags)
        self._flags.update(flags)

    def remove_flags(self, flags: set[IngredientFlag]) -> None:
        """Deletes flags."""
        if not flags.issubset(self._flags):
            raise KeyError("One or more flags not found in ingredient.")
        self._flags.difference_update(flags)

    def set_all_flags_true(self) -> None:
        """Sets all flags to True."""
        for flag in self.flags:
            flag.flag_value = True

    def set_all_flags_false(self) -> None:
        """Sets all flags to False."""
        for flag in self.flags:
            flag.flag_value = False

    def update_nutrient_quantities(self, nutrient_quantities: set[IngredientNutrientQuantity]) -> None:
        """Updates nutrient quantities."""
        self._nutrient_quantities.difference_update(nutrient_quantities)
        self._nutrient_quantities.update(nutrient_quantities)

    def remove_nutrient_quantities(self, nutrient_quantities: set[IngredientNutrientQuantity]) -> None:
        """Deletes nutrient quantities."""
        if not nutrient_quantities.issubset(self._nutrient_quantities):
            raise KeyError("One or more nutrient quantities not found in ingredient.")
        self._nutrient_quantities.difference_update(nutrient_quantities)

    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        if self.id == other.id and self.name == other.name:
            return True
        if self.id == other.id or self.name == other.name:
            raise ValueError("Either IDs match but names don't, or names match but IDs don't.")
        return False

    def __hash__(self):
        return hash((self.id, self.name))
