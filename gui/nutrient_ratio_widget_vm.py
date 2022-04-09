from PyQt6 import QtWidgets

from gui.nutrient_ratio_widget import NutrientRatioWidget

class NutrientRatioWidgetVM(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ui = NutrientRatioWidget()
        self.ui.setupUi(self)

