from typing import TYPE_CHECKING, TypedDict

from codiet.model.quantities import IsQuantified

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO
    from codiet.model.nutrients import Nutrient


class NutrientQuantityDTO(TypedDict):
    nutrient_name: str
    quantity: "QuantityDTO"


class NutrientQuantity(IsQuantified):

    def __init__(
        self,
        nutrient: "Nutrient",
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._nutrient = nutrient

    @property
    def nutrient(self) -> "Nutrient":
        return self._nutrient

    @property
    def calories(self) -> float:
        return self.nutrient.calories_per_gram * self.mass_in_grams

    def __hash__(self):
        return hash((self.nutrient.name))

    def __eq__(self, other):
        if not isinstance(other, NutrientQuantity):
            return False

        if self.nutrient.name != other.nutrient.name:
            return False

        return True

    def __str__(self):
        return f"{self.nutrient.name} quantity"
