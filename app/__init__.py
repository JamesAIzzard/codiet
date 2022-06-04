from PyQt6 import QtWidgets

# Expose the main GUI viewmodels
from .validators import (
    PositiveFloatValidator,
    Float0To100Validator
)
from .codiet_ctrl import CodietCtrl
from .codiet_combobox import CodietComboBox
from .flag_selector_view import FlagSelectorView
from .flag_selector_ctrl import FlagSelectorCtrl
from .nutrient_ratio_editor_view import NutrientRatioEditorView
from .nutrient_ratio_editor_ctrl import NutrientRatioEditorCtrl
from .search_widget_view import SearchWidgetView
from .search_widget_ctrl import SearchWidgetCtrl
from .ingredient_editor_view import IngredientEditorView
from .ingredient_editor_ctrl import IngredientEditorCtrl
from .user_requirements_editor_view import UserRequirementsEditorView
from .user_requirements_editor_ctrl import UserRequirementsEditorCtrl
from .mainwindow_view import MainWindowView
from .mainwindow_ctrl import MainWindowCtrl

def run() -> None:
    """Start the application."""
    # Instantiate the Qt application
    app = QtWidgets.QApplication([])
    # Instantiate the main window
    main_window_view = MainWindowView()
    main_window_ctrl = MainWindowCtrl(main_window_view)
    # Show the main window
    main_window_view.show()
    app.exec()