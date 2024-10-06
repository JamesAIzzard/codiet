from typing import TYPE_CHECKING, TypedDict

from codiet.model.quantities import IsQuantified

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO
    from codiet.model.nutrients import Nutrient


class NutrientQuantityDTO(TypedDict):
    nutrient_name: str
    nutrient_quantity: "QuantityDTO"


class NutrientQuantity(IsQuantified):

    def __init__(
        self,
        nutrient: "Nutrient",
        ingredient_grams_value: float | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._nutrient = nutrient
        self._ingredient_grams_value = ingredient_grams_value

    @property
    def nutrient(self) -> "Nutrient":
        return self._nutrient

    @property
    def ingredient_grams_value(self) -> float | None:
        return self._ingredient_grams_value

    @ingredient_grams_value.setter
    def ingredient_grams_value(self, value: float | None):
        self._ingredient_grams_value = value

    def __hash__(self):
        return hash((self.nutrient.name))

    def __eq__(self, other):
        if not isinstance(other, "NutrientQuantity"):
            return False

        if self.nutrient.name != other.nutrient.name:
            return False

        return True

    def __str__(self):
        return f"{self.nutrient.name} quantity"
