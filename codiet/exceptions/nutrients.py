class NutrientNotFoundError(ValueError):
    def __init__(self, nutrient_name: str):
        self.nutrient = nutrient_name
        self.message = f"Nutrient {nutrient_name} is not defined in the database."

    def __str__(self):
        return self.message