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
    
    @property
    def calories_per_gram(self) -> float:
        calories_total = 0

        for nutrient_quantity in self.nutrient_quantities.values():
            nutrient_grams = nutrient_quantity.mass_in_grams
            calories_total += nutrient_quantity.nutrient.calories_per_gram / nutrient_grams

        return calories_total