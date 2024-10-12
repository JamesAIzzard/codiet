from typing import Protocol, TYPE_CHECKING

from codiet.utils.unique_collection import ImmutableUniqueCollection as IUC

if TYPE_CHECKING:
    from codiet.model.quantities import UnitDTO, UnitConversionDTO
    from codiet.model.nutrients import NutrientDTO
    from codiet.model.flags import FlagDefinitionDTO
    from codiet.model.ingredients import IngredientDTO
    from codiet.model.recipes import RecipeDTO


class Repository(Protocol):
    def read_all_unit_names(self) -> IUC[str]: ...
    def read_unit_dto(self, name: str) -> "UnitDTO": ...
    def read_all_global_unit_conversion_names(self) -> IUC[frozenset[str]]: ...
    def read_global_unit_conversion_dto(
        self, names: frozenset[str]
    ) -> "UnitConversionDTO": ...
    def read_all_flag_names(self) -> IUC[str]: ...
    def read_flag_definition_dto(self, name: str) -> "FlagDefinitionDTO": ...
    def read_all_nutrient_names(self) -> IUC[str]: ...
    def read_nutrient_dto(self, name: str) -> "NutrientDTO": ...
    def read_all_ingredient_names(self) -> IUC[str]: ...
    def read_ingredient_dto(self, name: str) -> "IngredientDTO": ...
    def read_all_recipe_names(self) -> IUC[str]: ...
    def read_recipe_dto(self, name: str) -> "RecipeDTO": ...
