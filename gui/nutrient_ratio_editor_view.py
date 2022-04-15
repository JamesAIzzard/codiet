from PyQt6 import QtWidgets

from .nutrient_ratio_editor import Ui_nutrient_ratio_editor


class NutrientRatioEditor(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = Ui_nutrient_ratio_editor()
        self.ui.setupUi(self)