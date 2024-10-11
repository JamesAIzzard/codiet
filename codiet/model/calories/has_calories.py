from codiet.model.nutrients import HasNutrientQuantities

class HasCalories(HasNutrientQuantities):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def calories(self) -> float:
        calories_total = 0

        for nutrient_quantity in self.nutrient_quantities.values():
            calories_total += nutrient_quantity.calories

        return calories_total