from codiet.db.stored_entity import StoredEntity
from codiet.model.quantities.is_quantified import IsQuantified
from codiet.model.ingredients.ingredient import Ingredient

class IngredientQuantity(IsQuantified, StoredEntity):

    def __init__(
        self,
        ingredient: 'Ingredient',
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self._ingredient = ingredient

    @classmethod
    def from_ingredient_name(cls, ingredient_name: str) -> 'IngredientQuantity':
        ingredient = Ingredient(ingredient_name)
        return cls(ingredient=ingredient)
    
    @classmethod
    def from_ingredient(cls, ingredient: 'Ingredient') -> 'IngredientQuantity':
        return cls(ingredient=ingredient)

    @property
    def ingredient(self) -> 'Ingredient':
        if self._ingredient is None:
            raise TypeError("Ingredient not set.")
        return self._ingredient

    def __eq__(self, other):
        if not isinstance(other, IngredientQuantity):
            return False
        return (self.ingredient) == (other.ingredient)

    def __hash__(self):
        return hash(self.ingredient)
