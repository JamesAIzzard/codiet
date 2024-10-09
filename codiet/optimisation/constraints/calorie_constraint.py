from typing import TYPE_CHECKING

from codiet.optimisation.constraints.constraint import Constraint

if TYPE_CHECKING:
    from codiet.model.recipes import RecipeQuantity

class CalorieConstraint(Constraint):
    def __init__(self, required_calories: int) -> None:
        self.required_calories = required_calories

    def is_satisfied_by(self, recipe_quantity: "RecipeQuantity") -> bool:
        return recipe_quantity.calories == self.required_calories