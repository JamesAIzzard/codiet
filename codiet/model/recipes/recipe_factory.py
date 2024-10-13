from typing import TYPE_CHECKING

from codiet.model.recipes import Recipe

if TYPE_CHECKING:
    from codiet.model import SingletonRegister
    from codiet.model.quantities import QuantitiesFactory, UnitConversionService
    from codiet.model.flags import FlagFactory
    from codiet.model.time import TimeFactory
    from codiet.model.ingredients import IngredientFactory, IngredientQuantity
    from codiet.model.recipes import RecipeDTO


class RecipeFactory:
    def __init__(self):
        self._singleton_register: "SingletonRegister"
        self._unit_conversion_service: "UnitConversionService"
        self._quantities_factory: "QuantitiesFactory"
        self._time_factory: "TimeFactory"
        self._flag_factory: "FlagFactory"
        self._ingredient_factory: "IngredientFactory"

    def initialise(self,
            singleton_register: "SingletonRegister",
            unit_conversion_service: "UnitConversionService",
            quantities_factory: "QuantitiesFactory",
            time_factory: "TimeFactory",
            flag_factory: "FlagFactory",
            ingredient_factory: "IngredientFactory"           
        ) -> "RecipeFactory":
        self._singleton_register = singleton_register
        self._unit_conversion_service = unit_conversion_service
        self._quantities_factory = quantities_factory
        self._time_factory = time_factory
        self._flag_factory = flag_factory
        self._ingredient_factory = ingredient_factory

        return self

    def create_recipe_from_dto(self, recipe_dto: "RecipeDTO") -> "Recipe":
        ingredient_quantities:dict[str, "IngredientQuantity"] = {}
        for ingredient_name, ingredient_quantity_dto in recipe_dto[
            "ingredient_quantities"
        ].items():
            ingredient_quantity = (
                self._ingredient_factory.create_ingredient_quantity_from_dto(
                    ingredient_quantity_dto
                )
            )
            ingredient_quantities[ingredient_name] = ingredient_quantity

        serve_time_windows = []
        for time_window in recipe_dto["serve_time_windows"]:
            time_window = self._time_factory.create_time_window_from_dto(time_window)
            serve_time_windows.append(time_window)

        tags = []
        for tag_dto in recipe_dto["tags"]:
            tag = self._singleton_register.get_tag(tag_dto["name"])
            tags.append(tag)

        recipe = Recipe(
            name=recipe_dto["name"],
            use_as_ingredient=recipe_dto["use_as_ingredient"],
            description=recipe_dto["description"],
            instructions=recipe_dto["instructions"],
            ingredient_quantities=ingredient_quantities,
            serve_time_windows=serve_time_windows,
            tags=tags,
        )

        return recipe

    def create_recipe(self,
            name:str
        ) -> Recipe:
        recipe = Recipe(
            name=name,
            use_as_ingredient=False,
            description=None,
            instructions=[],
            ingredient_quantities={},
            serve_time_windows=[],
            tags=[],
        )
        return recipe
