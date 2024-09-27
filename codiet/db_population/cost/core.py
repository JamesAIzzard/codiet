from typing import Any

from codiet.db_population.quantities import build_quantity_from_json
from codiet.model.cost import QuantityCost

def build_quantity_cost_from_json(json_data:dict[str, Any]) -> QuantityCost:

    return QuantityCost(
        quantity=build_quantity_from_json(json_data["quantity"]),
        cost=json_data["cost"]
    )