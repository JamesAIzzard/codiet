from typing import TYPE_CHECKING

from codiet.model.ingredients import Ingredient, IngredientQuantity

if TYPE_CHECKING:
    from codiet.model import SingletonRegister
    from codiet.model.quantities import QuantitiesFactory, UnitConversionService
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
        self._nutrient_factory: "NutrientFactory"

    def initialise(
        self,
        singleton_register: "SingletonRegister",
        quantities_factory: "QuantitiesFactory",
        unit_conversion_service: "UnitConversionService",
        cost_factory: "CostFactory",
        flag_factory: "FlagFactory",
        nutrient_factory: "NutrientFactory",
    ) -> "IngredientFactory":
        self._singleton_register = singleton_register
        self._quantities_factory = quantities_factory
        self._unit_conversion_service = unit_conversion_service
        self._cost_factory = cost_factory
        self._flag_factory = flag_factory
        self._nutrient_factory = nutrient_factory

        IngredientQuantity.initialise(
            unit_conversion_service=self._unit_conversion_service,
            nutrient_factory=self._nutrient_factory
        )

        return self

    def create_ingredient_from_dto(self, ingredient_dto: "IngredientDTO") -> Ingredient:
        unit_conversions = {}
        for key, unit_conversion_dto in ingredient_dto["unit_conversions"].items():
            unit_conversion = self._quantities_factory.create_unit_conversion_from_dto(unit_conversion_dto)
            unit_conversions[key] = unit_conversion

        flags = {}
        for flag_name, flag_dto in ingredient_dto["flags"].items():
            flags[flag_name] = self._flag_factory.create_flag_from_dto(flag_dto)

        nutrient_quantities = {}
        for nutrient_name, nutrient_quantity_dto in ingredient_dto["nutrient_quantities_per_gram"].items():
            nutrient_quantity = self._nutrient_factory.create_nutrient_quantity_from_dto(nutrient_quantity_dto)
            nutrient_quantities[nutrient_name] = nutrient_quantity

        ingredient = Ingredient(
            name=ingredient_dto["name"],
            description=ingredient_dto["description"],
            unit_conversions=unit_conversions,
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
