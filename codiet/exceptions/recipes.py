class RecipeNotFoundError(FileNotFoundError):
    def __init__(self, recipe_name: str):
        super().__init__(f"Recipe '{recipe_name}' not found.")