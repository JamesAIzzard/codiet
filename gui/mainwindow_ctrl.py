import gui


class MainWindowCtrl:
    def __init__(self, view: gui.MainWindowView):
        self.view = view

        # Init the child controllers
        self.user_requirements_editor_ctrl = gui.UserRequirementsEditorCtrl(
            self.view.wg_page_stack.findChild(
                gui.UserRequirementsEditorView, "pg_user_reqs"
            ) # type: ignore
        )

        # Wire menu buttons to change page
        self.view.btn_add_ingredient.triggered.connect(
            lambda: self.view.change_window("pg_ingredient_editor")
        )
        self.view.btn_user_requirements.triggered.connect(
            lambda: self.view.change_window("pg_user_reqs")
        )
