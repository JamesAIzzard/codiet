from typing import Collection

from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
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
            global_units: Collection[Unit],
            global_unit_conversions: Collection[UnitConversion],   
            description:str|None=None,
            unit_conversions:Collection[IngredientUnitConversion]|None=None,
            standard_unit:Unit|None=None,
            cost_value:float|None=None,
            cost_qty_unit:Unit|None=None,
            cost_qty_value:float|None=None,
            flags:Collection[IngredientFlag]|None=None,
            gi:float|None=None,
            nutrient_quantities:Collection[IngredientNutrientQuantity]|None=None,
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
        self._flags = MUC(flags) or MUC()
        self._gi = gi
        self._nutrient_quantities = MUC(nutrient_quantities) or MUC()

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
    def unit_system(self) -> IngredientUnitsSystem:
        """Returns the unit system."""
        return self._unit_system

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
    def flags(self) -> IUC[IngredientFlag]:
        """Returns the flags."""
        return self._flags.immutable

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
    def nutrient_quantities(self) -> IUC[IngredientNutrientQuantity]:
        """Returns the nutrient quantities."""
        return self._nutrient_quantities.immutable

    def get_flag(self, flag_name: str) -> IngredientFlag:
        """Returns a flag by name."""
        for flag in self._flags:
            if flag.flag_name == flag_name:
                return flag
        raise KeyError(f"Flag {flag_name} not found in ingredient.")

    def add_flags(self, flags: IngredientFlag|Collection[IngredientFlag]) -> None:
        """Adds flags."""
        self._flags.add(flags)

    def update_flags(self, flags: IngredientFlag|Collection[IngredientFlag]) -> None:
        """Updates the flags passed in the set."""
        self._flags.update(flags)

    def remove_flags(self, flags: IngredientFlag|Collection[IngredientFlag]) -> None:
        """Deletes flags."""
        self._flags.remove(flags)

    def get_nutrient_quantity(self, nutrient_name: str) -> IngredientNutrientQuantity:
        """Returns a nutrient quantity by name."""
        for nutrient_quantity in self._nutrient_quantities:
            if nutrient_quantity.nutrient.nutrient_name == nutrient_name:
                return nutrient_quantity
        raise KeyError(f"Nutrient {nutrient_name} not found in ingredient.")

    def add_nutrient_quantities(self, nutrient_quantities: IngredientNutrientQuantity|Collection[IngredientNutrientQuantity]) -> None:
        """Adds nutrient quantities."""
        self._nutrient_quantities.add(nutrient_quantities)

    def update_nutrient_quantities(self, nutrient_quantities: IngredientNutrientQuantity|Collection[IngredientNutrientQuantity]) -> None:
        """Updates nutrient quantities."""
        self._nutrient_quantities.update(nutrient_quantities)

    def remove_nutrient_quantities(self, nutrient_quantities: IngredientNutrientQuantity|Collection[IngredientNutrientQuantity]) -> None:
        """Deletes nutrient quantities."""
        self._nutrient_quantities.remove(nutrient_quantities)

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
