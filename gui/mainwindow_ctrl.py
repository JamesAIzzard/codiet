from PyQt6 import QtWidgets

import gui


class MainWindowCtrl(gui.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the pages
        self.user_requirements_editor_ctrl = self.add_page(
            cls_controller=gui.UserRequirementsEditorCtrl,
            cls_view=gui.UserRequirementsEditorView,
            name="pg_user_reqs"
        )
        self.ingredient_editor_ctrl = self.add_page(
            cls_controller=gui.IngredientEditorCtrl,
            cls_view=gui.IngredientEditorView,
            name="pg_ingredient_editor"
        )

        # Wire menu buttons to change page
        self.view.btn_add_ingredient.triggered.connect(lambda: self.view.change_window("pg_ingredient_editor"))  # type: ignore
        self.view.btn_user_requirements.triggered.connect(lambda: self.view.change_window("pg_user_reqs"))  # type: ignore

    def add_page(self, name:str, cls_controller=gui.CodietCtrl, cls_view=QtWidgets.QWidget) -> gui.CodietCtrl:
        """Adds a page to the stack."""
        # Init the view
        view = cls_view()
        # Set its name so we can ID for page change
        view.setObjectName(name)
        # Init controller
        controller = cls_controller(view)
        # Insert view into stack
        self.view.add_page(view)  # type: ignore
        # Kick back the controller for reference
        return controller