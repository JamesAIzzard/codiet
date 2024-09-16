from typing import Collection, TYPE_CHECKING

from codiet.utils import MUC, IUC
from codiet.db.stored_entity import StoredEntity
from codiet.model.domain_service import UsesDomainService
from codiet.model.units import IngredientUnitSystem
from codiet.model.cost import CostRate

if TYPE_CHECKING:
    from codiet.model.units import Unit, UnitConversion
    from codiet.model.flags import Flag
    from codiet.model.nutrients import NutrientQuantity

class Ingredient(StoredEntity, UsesDomainService):
    """Ingredient model."""

    def __init__(
        self,
        name: str,
        description: str | None = None,
        unit_conversions: Collection['UnitConversion'] | None = None,
        standard_unit: 'Unit | None' = None,
        cost_rate: 'CostRate | None' = None,
        flags: Collection['Flag'] | None = None,
        gi: float | None = None,
        nutrient_quantities: Collection['NutrientQuantity'] | None = None,
        *args,
        **kwargs,
    ):
        """Initialises the class."""
        super().__init__(*args, **kwargs)

        self._name = name
        self._description = description
        self._unit_system = IngredientUnitSystem(
            ingredient=self,
            global_units=self.domain_service.global_units,
            global_unit_conversions=self.domain_service.global_unit_conversions,
            ingredient_unit_conversions=unit_conversions,
        )

        # If the standard unit is not set, just use grams
        if standard_unit is None:
            self._standard_unit = self._unit_system.gram
        else:
            # Check the standard unit is accessible
            if standard_unit not in self._unit_system.get_available_units():
                raise ValueError(
                    f"{standard_unit.name} is not accessible in the unit system."
                )
            self._standard_unit = standard_unit

        # Deal with the cost rate class
        self._cost_rate = cost_rate or CostRate()

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
            raise ValueError(f"{value.name} is not accessible in the unit system.")

        self._standard_unit = value

    @property
    def cost_rate(self) -> 'CostRate':
        """Returns the cost rate."""
        return self._cost_rate

    @property
    def flags(self) -> IUC['Flag']:
        """Returns the flags."""
        return IUC(self._flags)

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
    def nutrient_quantities(self) -> IUC['NutrientQuantity']:
        """Returns the nutrient quantities."""
        return self._nutrient_quantities.immutable

    def get_flag_by_name(self, flag_name: str) -> 'Flag':
        """Returns a flag by name."""
        for flag in self._flags:
            if flag.name == flag_name:
                return flag
        raise KeyError(f"Flag {flag_name} not found in ingredient.")

    def add_flag(self, flag: 'Flag') -> None:
        """Adds a flag."""
        self._flags.add(flag)

    def add_flags(self, flags: Collection['Flag']) -> None:
        """Adds multiple flags."""
        for flag in flags:
            self.add_flag(flag)

    def remove_flag(self, flag: 'Flag') -> None:
        """Deletes a flag."""
        self._flags.remove(flag)

    def get_nutrient_quantity_by_name(self, nutrient_name: str) -> 'NutrientQuantity':
        """Returns a nutrient quantity by name."""
        for nutrient_quantity in self._nutrient_quantities:
            if nutrient_quantity.nutrient.name == nutrient_name:
                return nutrient_quantity
        raise KeyError(f"Nutrient {nutrient_name} not found in ingredient.")

    def add_nutrient_quantity(
        self, nutrient_quantity: 'NutrientQuantity'
    ) -> None:
        """Adds a nutrient quantity."""
        self._nutrient_quantities.add(nutrient_quantity)

    def add_nutrient_quantities(self, nutrient_quantities: Collection['NutrientQuantity']) -> None:
        """Adds multiple nutrient quantities."""
        for nutrient_quantity in nutrient_quantities:
            self.add_nutrient_quantity(nutrient_quantity)

    def remove_nutrient_quantity(
        self,
        nutrient_quantity: 'NutrientQuantity'
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
