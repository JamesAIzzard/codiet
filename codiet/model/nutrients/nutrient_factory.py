from typing import TYPE_CHECKING

from codiet.model.nutrients import Nutrient, NutrientQuantity

if TYPE_CHECKING:
    from codiet.model.singleton_register import SingletonRegister
    from codiet.model.quantities import QuantitiesFactory
    from codiet.model.nutrients import NutrientDTO, NutrientQuantityDTO

class NutrientFactory:

    def __init__(self):
    
        self._singleton_register: "SingletonRegister"
        self._quantities_factory: "QuantitiesFactory"
    
    def create_nutrient_from_dto(self, nutrient_dto: "NutrientDTO") -> Nutrient:
        # Create the nutrient with children only (so working down the tree)
        children = {}
        for child_name in nutrient_dto["child_names"]:
            children[child_name] = self._singleton_register.get_nutrient(child_name)

        nutrient = Nutrient(
            name=nutrient_dto["name"],
            aliases=nutrient_dto.get("aliases", []),
            children=children
        )

        # Set the parent nutrient
        if nutrient_dto["parent_name"]:
            nutrient._parent = self._singleton_register.get_nutrient(nutrient_dto["parent_name"])

        return nutrient

    def create_nutrient_quantity_from_dto(self, nutrient_quantity_dto: "NutrientQuantityDTO") -> NutrientQuantity:
        nutrient_quantity = NutrientQuantity(
            nutrient=self._singleton_register.get_nutrient(nutrient_quantity_dto["nutrient_name"]),
            quantity=self._quantities_factory.create_quantity_from_dto(nutrient_quantity_dto["nutrient_quantity"]),
        )
        return nutrient_quantity