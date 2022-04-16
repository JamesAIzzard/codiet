import gui, data, model

class IngredientEditorCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load in a fresh ingredient instance
        self.ingredient = model.ingredients.Ingredient()

        # Wire the active elements
        self.view.btn_save_ingredient.clicked.connect(  # type: ignore
            self.on_save_ingredient
        )

    def on_save_ingredient(self) -> None:
        """Click handler for save ingredient button."""
        # Grab the name from the ingredient lineedit
        self.ingredient.name = self.view.txt_ingredient_name.text() # type: ignore
        data.save_ingredient(self.ingredient)