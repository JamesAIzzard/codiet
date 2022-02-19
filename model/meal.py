from typing import Dict

from model.calories import HasCalories

class Meal(HasCalories):
    """Models a meal.
    Meals are collections of ingredients, by ratio.
    """

    @property
    def ingredients(self) -> Dict[str, float]:
        """Returns dict of ingredient ID's and quantities in grams, currently associated with the meal."""
        raise NotImplementedError