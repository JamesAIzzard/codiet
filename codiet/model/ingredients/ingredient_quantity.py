from typing import TYPE_CHECKING, TypedDict

from codiet.model.quantities.is_quantified import IsQuantified
from codiet.model.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO, Quantity

class IngredientQuantityDTO(TypedDict):
    ingredient_name: str
    quantity: 'QuantityDTO'

class IngredientQuantity(IsQuantified):

    def __init__(
        self,
        ingredient: 'Ingredient',
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._ingredient = ingredient

    @property
    def ingredient(self) -> 'Ingredient':
        return self._ingredient

    def convert_to(self, unit_name: str) -> 'Quantity':
        return self.ingredient._unit_system.convert_quantity(self.quantity, to_unit_name=unit_name)

    def __eq__(self, other):
        if not isinstance(other, IngredientQuantity):
            return False
        return (self.ingredient) == (other.ingredient)

    def __hash__(self):
        return hash(self.ingredient)
