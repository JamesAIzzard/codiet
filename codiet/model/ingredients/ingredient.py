from typing import TYPE_CHECKING

from codiet.model.cost.quantity_cost import QuantityCost
from codiet.utils import IUC, UniqueDict
from codiet.db.stored_entity import StoredEntity
from codiet.model.domain_service import UsesDomainService
from codiet.model.cost import HasSettableQuantityCost
from codiet.model.quantities import UnitSystem
from codiet.model.flags import HasSettableFlags, Flag
from codiet.model.nutrients import HasSettableNutrientQuantities, NutrientQuantity

if TYPE_CHECKING:
    from codiet.model.quantities import Unit, UnitConversion, Quantity


class Ingredient(
    HasSettableQuantityCost,
    HasSettableNutrientQuantities,
    HasSettableFlags,
    StoredEntity,
    UsesDomainService,
):

    def __init__(
        self,
        name: str,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._name = name
        self._description: str | None = None
        self._unit_system = UnitSystem()
        self._standard_unit = self.domain_service.gram
        self._gi: float | None = None
        self._flags = UniqueDict[str, 'Flag']()
        self._nutrient_quantities = UniqueDict[str, 'NutrientQuantity']()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip().replace(" ", ""):
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def description(self) -> str | None:
        return self._description

    @description.setter
    def description(self, value: str | None) -> None:
        self._description = value

    @property
    def standard_unit(self) -> "Unit":
        return self._standard_unit

    @standard_unit.setter
    def standard_unit(self, unit: "Unit|str") -> None:
        if isinstance(unit, str):
            unit = self.domain_service.get_unit(unit)

        if not self._unit_system.check_unit_available(unit):
            raise ValueError(f"Unit {unit} is not available on {self.name}.")

        self._standard_unit = unit

    @property
    def quantity_cost(self) -> QuantityCost:
        if self._quantity_cost is None:
            raise ValueError("Quantity cost has not been set.")
        return self._quantity_cost

    @quantity_cost.setter
    def quantity_cost(self, value: QuantityCost) -> None:
        self.set_quantity_cost(value)

    @property
    def gi(self) -> float | None:
        return self._gi

    @gi.setter
    def gi(self, value: float | None) -> None:
        if value is not None and (value < 0 or value > 100):
            raise ValueError("GI must be between 0 and 100.")
        self._gi = value

    @property
    def flags(self) -> IUC["Flag"]:
        return IUC(self._flags.values())

    @property
    def nutrient_quantities(self) -> IUC["NutrientQuantity"]:
        return IUC(self._nutrient_quantities.values())

    def add_unit_conversion(self, unit_conversion: "UnitConversion") -> None:
        self._unit_system.add_entity_unit_conversion(unit_conversion)

    def set_quantity_cost(self, quantity_cost: QuantityCost) -> "Ingredient":
        if not self._unit_system.check_unit_available(quantity_cost.quantity.unit):
            raise ValueError(
                f"Unit {quantity_cost.quantity.unit} is not available on {self.name}."
            )

        self._quantity_cost = quantity_cost

        return self

    def get_flag(self, name: str) -> 'Flag':
        if not name in self.domain_service.flag_names:
            raise ValueError(f"Flag {name} is not known to the system.")
        
        try:
            return self._flags[name]
        except KeyError:
            self._add_flag(Flag(name))
            return self._flags[name]

    def set_flag(self, name: str, value: bool | None) -> 'Ingredient':
        self.get_flag(name).value = value
        
        return self

    def _add_flag(self, flag: Flag) -> 'Ingredient':
        if not flag.name in self.domain_service.flag_names:
            raise ValueError(f"Flag {flag.name} is not known to the system.")
        
        self._flags[flag.name] = flag

        return self

    def get_nutrient_quantity(self, nutrient_name: str) -> 'NutrientQuantity':
        try:
            return self._nutrient_quantities[nutrient_name]
        except KeyError:
            nutrient = self.domain_service.get_nutrient(nutrient_name)
            nutrient_quantity = NutrientQuantity(nutrient)
            self._add_nutrient_quantity(nutrient_quantity)
            return nutrient_quantity

    def set_nutrient_quantity(self, nutrient_name: str, quantity: 'Quantity') -> 'Ingredient':
        nutrient_quantity = self.get_nutrient_quantity(nutrient_name)
        nutrient_quantity.quantity = quantity
        return self

    def _add_nutrient_quantity(self, nutrient_quantity: "NutrientQuantity") -> "Ingredient":
        # TODO: Install any validation on the nutrient quantity
        self._nutrient_quantities[nutrient_quantity.nutrient.name] = nutrient_quantity
        return self

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
