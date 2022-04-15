from PyQt6 import QtWidgets, uic

import gui

class NutrientRatioEditorView(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Declare the active widgets
        # ...

        # Bring the ui file in
        uic.load_ui.loadUi('gui/nutrient_ratio_editor.ui', self)