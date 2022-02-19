from typing import List

from model import Ingredient

class Meal():
    """Models a meal.
    Meals are collections of ingredients, by ratio.
    """

    @property
    def ingredients(self) -> List[Ingredient]:
        """Returns the list of ingredients currently associated with the meal."""
        raise NotImplementedError