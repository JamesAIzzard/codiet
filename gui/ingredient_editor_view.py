from PyQt6 import QtWidgets, uic

import gui

class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Declare active widgets
        self.btn_save_ingredient: QtWidgets.QPushButton

        # Load in the ui file
        uic.load_ui.loadUi('gui/ingredient_editor.ui', self)