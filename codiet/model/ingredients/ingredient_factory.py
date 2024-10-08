from typing import TYPE_CHECKING

from codiet.model.ingredients import Ingredient, IngredientQuantity

if TYPE_CHECKING:
    from codiet.model import SingletonRegister
    from codiet.model.quantities import Quantity, QuantitiesFactory, QuantityDTO
    from codiet.model.cost import CostFactory
    from codiet.model.flags import FlagFactory
    from codiet.model.nutrients import NutrientFactory
    from codiet.model.ingredients import IngredientDTO, IngredientQuantityDTO    

class IngredientFactory:
    def __init__(self):

        self._singleton_register: "SingletonRegister"
        self._quantities_factory: "QuantitiesFactory"
        self._cost_factory: "CostFactory"
        self._flag_factory: "FlagFactory"
        self._nutrients_factory: "NutrientFactory"

    def create_ingredient_from_dto(self, ingredient_dto: "IngredientDTO") -> Ingredient:
        flags = {}
        for flag_name, flag_dto in ingredient_dto["flags"].items():
            flags[flag_name] = self._flag_factory.create_flag_from_dto(flag_dto)

        nutrient_quantities = {}
        for nutrient_name, nutrient_quantity_dto in ingredient_dto["nutrient_quantities_per_gram"].items():
            nutrient_quantity = self._nutrients_factory.create_nutrient_quantity_from_dto(nutrient_quantity_dto)
            nutrient_quantities[nutrient_name] = nutrient_quantity

        ingredient = Ingredient(
            name=ingredient_dto["name"],
            description=ingredient_dto["description"],
            unit_system=self._quantities_factory.create_unit_system(),
            standard_unit=self._singleton_register.get_unit(ingredient_dto["standard_unit"]),
            quantity_cost=self._cost_factory.create_quantity_cost_from_dto(ingredient_dto["quantity_cost"]),
            gi=ingredient_dto["gi"],
            flags=flags,
            nutrient_quantities_per_gram=nutrient_quantities
        )
        return ingredient

    def create_ingredient_quantity_from_dto(self, ingredient_quantity_dto:"IngredientQuantityDTO") -> "IngredientQuantity":
        ingredient = self._singleton_register.get_ingredient(ingredient_quantity_dto["ingredient_name"])
        quantity = self._quantities_factory.create_quantity_from_dto(ingredient_quantity_dto["quantity"])
        ingredient_quantity = IngredientQuantity(ingredient, quantity)
        return ingredient_quantity
    
    def create_ingredient_quantity(self, ingredient_name:str, quantity_unit_name:str, quantity_value:float) -> "IngredientQuantity":
        ingredient = self._singleton_register.get_ingredient(ingredient_name)
        quantity = self._quantities_factory.create_quantity(unit_name=quantity_unit_name, value=quantity_value)
        ingredient_quantity = IngredientQuantity(ingredient, quantity)
        return ingredient_quantity
