from typing import TYPE_CHECKING

from codiet.model.quantities import Unit, Quantity, UnitSystem

if TYPE_CHECKING:
    from codiet.model.singleton_register import SingletonRegister
    from codiet.model.quantities import UnitDTO, QuantityDTO

class QuantitiesFactory:
    
    def __init__(self):

        self._singleton_register: "SingletonRegister"

    def set_singleton_register(self, singleton_register: "SingletonRegister") -> "QuantitiesFactory":
        self._singleton_register = singleton_register
        return self

    def create_unit_from_dto(self, unit_dto: "UnitDTO") -> Unit:
        unit = Unit(
            name=unit_dto["name"],
            type=unit_dto["type"],
            singular_abbreviation=unit_dto["singular_abbreviation"],
            plural_abbreviation=unit_dto["plural_abbreviation"],
            aliases=unit_dto["aliases"],
        )
        return unit

    def create_unit_system(self) -> "UnitSystem":
        return UnitSystem()

    def create_quantity_from_dto(self, quantity_dto: "QuantityDTO") -> Quantity:
        quantity = Quantity(
            unit=self._singleton_register.get_unit(quantity_dto["unit_name"]),
            value=quantity_dto["value"],
        )
        return quantity