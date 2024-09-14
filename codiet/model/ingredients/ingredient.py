from typing import Collection, TYPE_CHECKING

from codiet.utils.unique_collection import MutableUniqueCollection as MUC
from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC
from codiet.db.stored_entity import StoredEntity
from codiet.model.units.ingredient_units_system import IngredientUnitsSystem

if TYPE_CHECKING:
    from codiet.model.units.unit import Unit
    from codiet.model.units.unit_conversion import GlobalUnitConversion
    from codiet.model.units.ingredient_unit_conversion import IngredientUnitConversion
    from codiet.model.flags.ingredient_flag import IngredientFlag
    from codiet.model.nutrients.ingredient_nutrient_quantity import (
        IngredientNutrientQuantity,
    )

if TYPE_CHECKING:
    from codiet.db.database_service.unit_db_service import UnitDBService


class Ingredient(StoredEntity):
    """Ingredient model."""

    # Class-level attributes for global units and conversions
    _global_units: IUC['Unit']
    _global_unit_conversions: IUC['GlobalUnitConversion']

    @classmethod
    def initialise_class(
        cls,
        global_units: Collection['Unit'],
        global_unit_conversions: Collection['GlobalUnitConversion'],
    ):
        """Initialize class-level attributes from UnitDBService."""
        cls._global_units = IUC(global_units)
        cls._global_unit_conversions = IUC(global_unit_conversions)

    def __init__(
        self,
        name: str,
        description: str | None = None,
        unit_conversions: Collection['IngredientUnitConversion'] | None = None,
        standard_unit: 'Unit | None' = None,
        cost_value: float | None = None,
        cost_qty_unit: 'Unit | None' = None,
        cost_qty_value: float | None = None,
        flag_ids: MUC[int] | None = None,
        gi: float | None = None,
        nutrient_quantity_ids: MUC[int] | None = None,
        *args,
        **kwargs,
    ):
        """Initializes the class."""
        super().__init__(*args, **kwargs)

        if self._global_units is None or self._global_unit_conversions is None:
            raise RuntimeError(
                "Ingredient class has not been initialized. Call Ingredient.initialize_class() first."
            )

        self._name = name
        self._description = description
        self._unit_system = IngredientUnitsSystem(
            ingredient=self,
            global_units=Ingredient._global_units,
            global_unit_conversions=Ingredient._global_unit_conversions,
            ingredient_unit_conversions=unit_conversions,
        )

        # If the standard unit is not set, just use grams
        if standard_unit is None:
            self._standard_unit = self._unit_system.gram
        else:
            # Check the standard unit is accessible
            if standard_unit not in self._unit_system.get_available_units():
                raise ValueError(
                    f"{standard_unit.unit_name} is not accessible in the unit system."
                )
            self._standard_unit = standard_unit

        self._cost_value = cost_value

        # If the cost quantity unit is not set, set it to the standard unit
        if cost_qty_unit is None:
            self._cost_qty_unit = self._standard_unit
        else:
            # Check the cost quantity unit is accessible
            if cost_qty_unit not in self._unit_system.get_available_units():
                raise ValueError(
                    f"{cost_qty_unit.unit_name} is not accessible in the unit system."
                )
            self._cost_qty_unit = cost_qty_unit

        self._cost_qty_value = cost_qty_value
        self._flags = MUC(flag_ids) or MUC()
        self._gi = gi
        self._nutrient_quantities = MUC(nutrient_quantity_ids) or MUC()

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
    def standard_unit(self) -> 'Unit':
        """Returns the standard unit ID."""
        return self._standard_unit

    @standard_unit.setter
    def standard_unit(self, value: 'Unit') -> None:
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
    def cost_qty_unit(self) -> 'Unit':
        """Returns the cost quantity unit."""
        return self._cost_qty_unit

    @cost_qty_unit.setter
    def cost_qty_unit(self, value: 'Unit') -> None:
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
    def flags(self) -> IUC['IngredientFlag']:
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
    def nutrient_quantities(self) -> IUC['IngredientNutrientQuantity']:
        """Returns the nutrient quantities."""
        return self._nutrient_quantities.immutable

    def get_flag(self, flag_name: str) -> 'IngredientFlag':
        """Returns a flag by name."""
        for flag in self._flags:
            if flag.flag_name == flag_name:
                return flag
        raise KeyError(f"Flag {flag_name} not found in ingredient.")

    def add_flag(self, flag: 'IngredientFlag') -> None:
        """Adds a flag."""
        self._flags.add(flag)

    def remove_flag(self, flag: 'IngredientFlag') -> None:
        """Deletes a flag."""
        self._flags.remove(flag)

    def get_nutrient_quantity(self, nutrient_name: str) -> 'IngredientNutrientQuantity':
        """Returns a nutrient quantity by name."""
        for nutrient_quantity in self._nutrient_quantities:
            if nutrient_quantity.nutrient.nutrient_name == nutrient_name:
                return nutrient_quantity
        raise KeyError(f"Nutrient {nutrient_name} not found in ingredient.")

    def add_nutrient_quantity(
        self, nutrient_quantity: 'IngredientNutrientQuantity'
    ) -> None:
        """Adds a nutrient quantity."""
        self._nutrient_quantities.add(nutrient_quantity)

    def remove_nutrient_quantity(
        self,
        nutrient_quantity: 'IngredientNutrientQuantity'
    ) -> None:
        """Deletes nutrient quantities."""
        self._nutrient_quantities.remove(nutrient_quantity)

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
