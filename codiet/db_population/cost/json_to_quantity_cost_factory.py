from codiet.db_population import JSONToObjectFactory
from codiet.model.cost import QuantityCost

class JSONToQuantityCostFactory(JSONToObjectFactory):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def build(self) -> QuantityCost:
        cost_quantity = QuantityCost()
        cost_quantity.cost = self.json["cost"]
        cost_quantity.quantity = self.json["quantity"]
        return cost_quantity