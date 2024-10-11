from typing import TYPE_CHECKING

from codiet.model.quantities import Unit, Quantity, UnitConversion

if TYPE_CHECKING:
    from codiet.data import DatabaseService
    from codiet.model.singleton_register import SingletonRegister
    from codiet.model.quantities import UnitDTO, QuantityDTO, UnitConversionDTO, UnitConversionService


class QuantitiesFactory:

    def __init__(self):

        self._singleton_register: "SingletonRegister"
        self._database_service: "DatabaseService"

    def initialise(
        self,
        singleton_register: "SingletonRegister",
        database_service: "DatabaseService",
        unit_conversion_service: "UnitConversionService",
    ) -> "QuantitiesFactory":
        self._singleton_register = singleton_register
        self._database_service = database_service
        self._unit_conversion_service = unit_conversion_service

        Quantity.initialise(unit_conversion_service=self._unit_conversion_service)

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

    def create_unit_conversion_from_dto(
        self, unit_conversion_dto: "UnitConversionDTO"
    ) -> "UnitConversion":
        from_quantity = self.create_quantity_from_dto(
            unit_conversion_dto["from_quantity"]
        )
        to_quantity = self.create_quantity_from_dto(unit_conversion_dto["to_quantity"])
        unit_conversion = UnitConversion(
            from_quantity=from_quantity, to_quantity=to_quantity
        )
        return unit_conversion

    def create_unit_conversion(
        self,
        from_unit_name: str,
        from_unit_quantity: float,
        to_unit_name: str,
        to_unit_quantity: float,
    ) -> "UnitConversion":
        return UnitConversion(
            from_quantity=self.create_quantity(
                unit_name=from_unit_name, value=from_unit_quantity
            ),
            to_quantity=self.create_quantity(
                unit_name=to_unit_name, value=to_unit_quantity
            ),
        )

    def create_quantity_from_dto(self, quantity_dto: "QuantityDTO") -> Quantity:
        quantity = Quantity(
            unit=self._singleton_register.get_unit(quantity_dto["unit_name"]),
            value=quantity_dto["value"],
        )
        return quantity

    def create_quantity(self, unit_name: str, value: float) -> Quantity:
        return Quantity(
            unit=self._singleton_register.get_unit(unit_name=unit_name), value=value
        )
