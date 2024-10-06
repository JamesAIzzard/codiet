from typing import TYPE_CHECKING, TypedDict

from codiet.model.stored_entity import StoredEntity
from codiet.model.quantities.is_quantified import IsQuantified
from codiet.model.ingredients.ingredient import Ingredient

if TYPE_CHECKING:
    from codiet.model.quantities import QuantityDTO

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

    def __eq__(self, other):
        if not isinstance(other, IngredientQuantity):
            return False
        return (self.ingredient) == (other.ingredient)

    def __hash__(self):
        return hash(self.ingredient)
