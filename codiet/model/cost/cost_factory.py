from typing import TYPE_CHECKING

from codiet.model.cost import QuantityCost

if TYPE_CHECKING:
    from codiet.model.quantities import QuantitiesFactory
    from codiet.model.cost import QuantityCostDTO

class CostFactory:
    
    def __init__(self) -> None:
        self._quantities_factory: "QuantitiesFactory"

    def create_quantity_cost_from_dto(self, quantity_cost_dto: "QuantityCostDTO") -> QuantityCost:
        quantity_cost = QuantityCost(
            cost=quantity_cost_dto["cost"],
            quantity=self._quantities_factory.create_quantity_from_dto(quantity_cost_dto["quantity"]),
        )
        return quantity_cost