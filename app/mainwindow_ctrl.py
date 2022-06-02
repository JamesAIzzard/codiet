from PyQt6 import QtWidgets

import app


class MainWindowCtrl(app.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Hint the view
        self.view: app.MainWindowView

        # Add the pages
        self.user_requirements_editor_ctrl = self._add_page(
            cls_controller=app.UserRequirementsEditorCtrl,
            cls_view=app.UserRequirementsEditorView,
            name="pg_user_reqs",
        )
        self.ingredient_editor_ctrl = self._add_page(
            cls_controller=app.IngredientEditorCtrl,
            cls_view=app.IngredientEditorView,
            name="pg_ingredient_editor",
        )

        # Wire menu buttons to change page
        self.view.btn_ingredients.triggered.connect(lambda: self.view.change_window("pg_ingredient_editor"))
        self.view.btn_user_requirements.triggered.connect(lambda: self.view.change_window("pg_user_reqs"))

        # Set the loading page
        self.view.change_window("pg_ingredient_editor")

    def _add_page(
        self, name: str, cls_controller=app.CodietCtrl, cls_view=QtWidgets.QWidget
    ) -> app.CodietCtrl:
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
