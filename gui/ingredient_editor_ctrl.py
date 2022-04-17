from PyQt6 import QtWidgets

import gui, data, model

class IngredientEditorCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out the view type for intellisense
        self.view: gui.IngredientEditorView

        # Insert the flag editor widget
        flag_selector_view = gui.FlagSelectorView()
        self.flag_selector_ctrl = gui.FlagSelectorCtrl(
            view=flag_selector_view,
            on_flag_adoption_callback=lambda flag_string: print(f"{flag_string} adopted"),
            on_flag_removal_callback=lambda flag_string: print(f"{flag_string} removed")
        )
        vbox = QtWidgets.QVBoxLayout()
        vbox.addWidget(flag_selector_view)
        self.view.wg_flags.setLayout(vbox)

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