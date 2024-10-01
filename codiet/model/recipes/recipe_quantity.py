from codiet.model.quantities.is_quantified import IsQuantified

class RecipeQuantity(IsQuantified):

    def __init__(self, quantity:float, unit:str, recipe:str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._quantity = quantity
        self._unit = unit
        self._name = recipe

    @property
    def recipe(self) -> str:
        return self._recipe
    
    @recipe.setter
    def recipe(self, recipe:str):
        self._recipe = recipe
