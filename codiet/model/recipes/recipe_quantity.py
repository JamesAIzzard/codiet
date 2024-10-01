from codiet.model.quantities.is_quantified import IsQuantified

class RecipeQuantity(IsQuantified):

    def __init__(self, recipe:str , *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._recipe = recipe

    @property
    def recipe(self) -> str:
        return self._recipe
    
    @recipe.setter
    def recipe(self, recipe:str):
        self._recipe = recipe
