from typing import Any

from codiet.model.domain_service import DomainService
from codiet.model.quantities import UnitConversion, Quantity

def build_quantity_from_json(json_data:list[str|float]) -> Quantity:
    """Expects a json list with one string and one float,
        for example: ["gram", 1.0]
    """

    domain_service = DomainService.get_instance()

    unit_name, value = _identify_unit_name_and_quantity(json_data)

    unit = domain_service.get_unit(unit_name)

    return Quantity(
        unit=unit,
        value=value
    )

def build_unit_conversion_from_json(json_data:list[list[str|float]]) -> UnitConversion:
    """Expects a list of two json lists with one string and one float each,
        for example: [["gram", 1.0], [kilogram", 0.001]]
    """

    first_quantity = build_quantity_from_json(json_data[0])
    second_quantity = build_quantity_from_json(json_data[1])

    return UnitConversion((first_quantity, second_quantity))

def _identify_unit_name_and_quantity(json_data:list[str|float]) -> tuple[str, float]:
    if type(json_data[0]) == str:
        unit_name = json_data[0]
        unit_quantity = json_data[1]
    else:
        unit_name = json_data[1]
        unit_quantity = json_data[0]    

    return (unit_name, unit_quantity) # type: ignore