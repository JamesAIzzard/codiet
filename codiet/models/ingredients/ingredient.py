from codiet.db.stored_entity import StoredEntity
from codiet.models.units.unit import Unit
from codiet.models.units.unit_conversion import UnitConversion
from codiet.models.units.ingredient_unit_conversion import IngredientUnitConversion
from codiet.models.units.ingredient_units_system import IngredientUnitsSystem
from codiet.models.flags.ingredient_flag import IngredientFlag
from codiet.models.nutrients.ingredient_nutrient_quantity import IngredientNutrientQuantity


class Ingredient(StoredEntity):
    """Ingredient model."""

    def __init__(
            self, 
            name:str,
            global_units: set[Unit],
            global_unit_conversions: set[UnitConversion],   
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
        self._unit_system = IngredientUnitsSystem(
            ingredient=self,
            global_units=global_units,
            global_unit_conversions=global_unit_conversions,
            ingredient_unit_conversions=unit_conversions
        )

        # If the standard unit is not set, just use grams
        if standard_unit is None:
            self._standard_unit = self._unit_system.gram
        else:
            # Check the standard unit is accessible
            if standard_unit not in self._unit_system.get_available_units():
                raise ValueError(f"{standard_unit.unit_name} is not accessible in the unit system.")
            self._standard_unit = standard_unit
        
        self._cost_value = cost_value

        # If the cost quantity unit is not set, set it to the standard unit
        if cost_qty_unit is None:
            self._cost_qty_unit = self._standard_unit
        else:
            # Check the cost quantity unit is accessible
            if cost_qty_unit not in self._unit_system.get_available_units():
                raise ValueError(f"{cost_qty_unit.unit_name} is not accessible in the unit system.")
            self._cost_qty_unit = cost_qty_unit

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
    def description(self) -> str | None:
        """Returns the description."""
        return self._description
    
    @description.setter
    def description(self, value: str | None) -> None:
        """Sets the description."""
        self._description = value

    @property
    def standard_unit(self) -> Unit:
        """Returns the standard unit ID."""
        return self._standard_unit
    
    @standard_unit.setter
    def standard_unit(self, value: Unit) -> None:
        """Sets the standard unit ID."""
        if value is None:
            raise ValueError("Standard unit cannot be empty.")
        
        # Check the standard unit is accessible
        if value not in self._unit_system.get_available_units():
            raise ValueError(f"{value.unit_name} is not accessible in the unit system.")

        self._standard_unit = value

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
        return self._cost_qty_unit
    
    @cost_qty_unit.setter
    def cost_qty_unit(self, value: Unit) -> None:
        """Sets the cost quantity unit ID."""
        if value is None:
            raise ValueError("Cost quantity unit cannot be empty.")
        if value not in self._unit_system.get_available_units():
            raise ValueError(f"{value.unit_name} is not accessible in the unit system.")
        self._cost_qty_unit = value

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
    def gi(self) -> float | None:
        """Returns the GI."""
        return self._gi
    
    @gi.setter
    def gi(self, value: float | None) -> None:
        """Sets the GI."""
        if value is not None and (value < 0 or value > 100):
            raise ValueError("GI must be between 0 and 100.")
        self._gi = value

    @property
    def nutrient_quantities(self) -> frozenset[IngredientNutrientQuantity]:
        """Returns the nutrient quantities."""
        return frozenset(self._nutrient_quantities)

    @nutrient_quantities.setter
    def nutrient_quantities(self, value: set[IngredientNutrientQuantity]) -> None:
        """Sets the nutrient quantities."""
        self._nutrient_quantities = value

    def flag_value(self, flag_name: str) -> bool:
        """Returns the value of a flag."""
        for flag in self.flags:
            if flag.flag_name == flag_name:
                return flag.flag_value
        raise KeyError(f"Flag {flag_name} not found in ingredient.")

    def update_flags(self, flags: set[IngredientFlag]) -> None:
        """Updates the flags passed in the set."""
        self._flags.difference_update(flags)
        self._flags.update(flags)

    def remove_flags(self, flags: set[IngredientFlag]) -> None:
        """Deletes flags."""
        if not flags.issubset(self._flags):
            raise KeyError("One or more flags not found in ingredient.")
        self._flags.difference_update(flags)

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
        # If on either instance, the name and ID is None, raise exception
        if self.id is None and self.name is None:
            raise ValueError("Ingredient must have an ID or a name for comparison.")
        # If either ID is None, match on  names
        if self.id is None or other.id is None:
            return self.name == other.name
        # If both IDs are set, match on IDs
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.name))
