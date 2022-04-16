from PyQt6 import QtWidgets, uic

class IngredientEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Load in the ui file
        uic.load_ui.loadUi('gui/ingredient_editor.ui', self)