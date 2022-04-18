from PyQt6 import QtWidgets, uic

class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out active elements for intellisense
        self.wg_flags: QtWidgets.QGroupBox

        # Load in the ui file
        uic.load_ui.loadUi('gui/ingredient_editor.ui', self)