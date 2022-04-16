import gui

class IngredientEditorCtrl:
    def __init__(self, view: gui.IngredientEditorView):
        self.view = view

        # Wire the active elements
        self.view.btn_save_ingredient.clicked.connect(
            self.on_save_ingredient
        )

    def on_save_ingredient(self):
        """Click handler for save ingredient button."""
        print("save ingredient pressed.")