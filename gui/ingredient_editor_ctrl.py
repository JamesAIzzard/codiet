import gui

class IngredientEditorCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Wire the active elements
        self.view.btn_save_ingredient.clicked.connect(  # type: ignore
            self.on_save_ingredient
        )

    def on_save_ingredient(self) -> None:
        """Click handler for save ingredient button."""
        print("save ingredient pressed.")