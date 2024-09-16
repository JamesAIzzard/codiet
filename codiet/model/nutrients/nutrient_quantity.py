"""Models a nutrient quantity."""

from typing import TYPE_CHECKING

from codiet.db.stored_entity import StoredEntity
from codiet.model.quantity.is_quantity import IsQuantity
from codiet.model.nutrients.nutrient import Nutrient

if TYPE_CHECKING:
    from codiet.model.ingredients.ingredient import Ingredient


class NutrientQuantity(IsQuantity, StoredEntity):
    """Class to represent the nutrient quantity associated with an entity."""

    def __init__(
        self,
        nutrient: Nutrient,
        ingredient_grams_value: float | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self._nutrient = nutrient
        self._ingredient_grams_value = ingredient_grams_value

    @property
    def nutrient(self) -> Nutrient:
        """Return the nutrient."""
        return self._nutrient

    @property
    def ingredient_grams_qty(self) -> float | None:
        """Return the entity grams quantity."""
        return self._ingredient_grams_value

    @ingredient_grams_qty.setter
    def ingredient_grams_qty(self, value: float | None):
        """Set the entity grams quantity."""
        self._ingredient_grams_value = value

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
