from PyQt6 import QtWidgets

import gui, data, model

class IngredientEditorCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out the view type for intellisense
        self.view: gui.IngredientEditorView

        # Init controller for flag selector widget
        self.flag_selector_ctrl = gui.FlagSelectorCtrl(
            view=self.view.wg_flag_selector,
            on_flag_adoption_callback=self.on_flag_adopt,
            on_flag_removal_callback=self.on_flag_remove
        )

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

    def on_flag_adopt(self, flag_str:str) -> None:
        """Handler function for flag adoption."""
        pass

    def on_flag_remove(self, flag_str:str) -> None:
        """Hander function for flag removal."""
        pass