class IngredientNameExistsError(ValueError):
    def __init__(self, ingredient_name: str):
        self.ingredient_name = ingredient_name
        self.message = f"Ingredient with name '{ingredient_name}' already exists."
        super().__init__(self.message)