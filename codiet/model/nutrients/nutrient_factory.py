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
    
    def initialise(
        self,
        singleton_register: "SingletonRegister",
        quantities_factory: "QuantitiesFactory",
    ) -> "NutrientFactory":
        self._singleton_register = singleton_register
        self._quantities_factory = quantities_factory
        return self

    def create_nutrient_from_dto(self, nutrient_dto: "NutrientDTO") -> Nutrient:
        # Create the nutrient with children only (so working down the tree)
        children = {}
        for child_name in nutrient_dto["direct_child_names"]:
            children[child_name] = self._singleton_register.get_nutrient(child_name)

        nutrient = Nutrient(
            name=nutrient_dto["name"],
            calories_per_gram=nutrient_dto["cals_per_gram"],
            aliases=nutrient_dto.get("aliases", []),
            direct_children=children
        )

        # We need to add the nutrient to the singleton register before populating
        # the parent nutrient, so we can access it
        if nutrient.name not in self._singleton_register._nutrients:
            self._singleton_register._nutrients[nutrient.name] = nutrient

        # Set the parent nutrient
        if nutrient_dto["direct_parent_name"]:
            nutrient._direct_parent = self._singleton_register.get_nutrient(nutrient_dto["direct_parent_name"])

        return nutrient

    def create_nutrient_quantity_from_dto(self, nutrient_quantity_dto: "NutrientQuantityDTO") -> NutrientQuantity:
        nutrient_quantity = NutrientQuantity(
            nutrient=self._singleton_register.get_nutrient(nutrient_quantity_dto["nutrient_name"]),
            quantity=self._quantities_factory.create_quantity_from_dto(nutrient_quantity_dto["quantity"]),
        )
        return nutrient_quantity
    
    def create_nutrient_quantity(
        self,
        nutrient_name: str,
        quantity_value: float,
        quantity_unit_name: str
    ) -> NutrientQuantity:
        nutrient_quantity = NutrientQuantity(
            nutrient=self._singleton_register.get_nutrient(nutrient_name),
            quantity=self._quantities_factory.create_quantity(
                value=quantity_value,
                unit_name=quantity_unit_name
            )
        )
        return nutrient_quantity