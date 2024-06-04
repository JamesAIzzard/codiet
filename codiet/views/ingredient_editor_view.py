from PyQt6.QtWidgets import (
    QWidget,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QToolBar,
    QLabel,
    QGroupBox,
    QComboBox
)
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.utils.pyqt import block_signals
from codiet.views.buttons import (
    AddButton, 
    DeleteButton, 
    EditButton, 
    SaveJSONButton, 
    AutopopulateButton
)
from codiet.views.search import SearchColumnView
from codiet.views.nutrients import NutrientQuantitiesEditorView
from codiet.views.text_editors import LineEdit, MultilineEdit, NumericLineEdit
from codiet.views.flags import FlagEditorView
from codiet.views.units import CustomUnitsDefinitionView

class IngredientEditorView(QWidget):
    """User interface for editing an ingredient."""
    # Define signals
    searchTextChanged = pyqtSignal(str)
    searchTextCleared = pyqtSignal()
    ingredientSelected = pyqtSignal(str)
    addIngredientClicked = pyqtSignal()
    deleteIngredientClicked = pyqtSignal()
    autopopulateClicked = pyqtSignal()
    saveJSONClicked = pyqtSignal()
    editIngredientNameClicked = pyqtSignal()
    ingredientDescriptionChanged = pyqtSignal(str)
    ingredientCostValueChanged = pyqtSignal(QVariant)
    ingredientCostQuantityChanged = pyqtSignal(QVariant)
    ingredientCostQuantityUnitChanged = pyqtSignal(str)
    ingredientGIChanged = pyqtSignal(QVariant)


    def __init__(self):
        super().__init__()
        self._build_ui()

    def update_name(self, name: str | None):
        """Set the name of the ingredient."""
        with block_signals(self.txt_ingredient_name):
            if name is not None:
                self.txt_ingredient_name.setText(name)
            else:
                self.txt_ingredient_name.clear()

    def update_description(self, description: str | None):
        """Set the description of the ingredient."""
        with block_signals(self.txt_description):
            if description is not None:
                self.txt_description.setText(description)
            else:
                self.txt_description.clear()

    def update_cost_value(self, cost: float | None):
        """Set the cost value."""
        with block_signals(self.txt_cost):
            if cost is not None:
                self.txt_cost.setText(cost)
            else:
                self.txt_cost.clear()

    def update_cost_qty_value(self, cost_qty: float | None):
        """Set the cost quantity value."""
        with block_signals(self.txt_cost_quantity):
            if cost_qty is not None:
                self.txt_cost_quantity.setText(cost_qty)
            else:
                self.txt_cost_quantity.clear()

    def update_cost_qty_unit(self, cost_qty_unit: str):
        """Set the cost quantity unit."""
        with block_signals(self.cmb_cost_qty_unit):
            self.cmb_cost_qty_unit.setCurrentText(cost_qty_unit)

    def update_gi(self, gi: float | None):
        """Set the GI value in the GI textbox."""
        with block_signals(self.txt_gi):
            if gi is None:
                self.txt_gi.clear()
            else:
                self.txt_gi.setText(gi)

    def _build_ui(self):
        """Build the UI for the ingredient editor page."""
        # Create a top level layout
        lyt_top_level = QVBoxLayout()
        lyt_top_level.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lyt_top_level)

        # Put the toolbar in it
        self._build_toolbar(lyt_top_level)

        # Create a horizontal layout for the columns
        lyt_columns = QHBoxLayout()
        lyt_columns.setContentsMargins(5, 5, 5, 5)
        lyt_top_level.addLayout(lyt_columns)

        # Create a col for searching ingredients
        lyt_search_column = QVBoxLayout()
        # Reduce vertical padding
        lyt_search_column.setContentsMargins(0, 0, 0, 0)
        lyt_columns.addLayout(lyt_search_column, 1)
        self._build_search_ui(lyt_search_column)

        # Create a col for the basic info, cost, flags and GI
        lyt_first_col = QVBoxLayout()
        lyt_columns.addLayout(lyt_first_col, 2)
        self._build_basic_info_UI(lyt_first_col)
        # Add the cost editor to the column 1 layout
        self._build_cost_UI(lyt_first_col)
        # Add the measurement definition view
        self.custom_units_view = CustomUnitsDefinitionView()
        lyt_first_col.addWidget(self.custom_units_view)
        # Add the flags widget to the column1 layout
        self.flag_editor = FlagEditorView()
        lyt_first_col.addWidget(self.flag_editor)
        # Add the GI widget to the column1 layout
        self._build_gi_UI(lyt_first_col)
        # Add stretch to end of layout
        lyt_first_col.addStretch(1)

        # Create a second column for the nutrients editor
        lyt_nutrients_col = QVBoxLayout()
        lyt_nutrients_col.setContentsMargins(0, 0, 0, 0)
        lyt_columns.addLayout(lyt_nutrients_col, 1)
        # Add a groupbox
        gb_nutrients = QGroupBox("Nutrients")
        lyt_nutrients_col.addWidget(gb_nutrients)
        # Add a vertical layout to the groupbox
        lyt_nutrients = QVBoxLayout()
        lyt_nutrients.setContentsMargins(0, 0, 0, 0)
        gb_nutrients.setLayout(lyt_nutrients)
        self.nutrient_quantities_editor = NutrientQuantitiesEditorView()
        lyt_nutrients.addWidget(self.nutrient_quantities_editor)

    def _build_toolbar(self, container: QBoxLayout) -> None:
        """Builds the main page toolbar."""
        # Build the toolbar
        toolbar = QToolBar(self)
        container.addWidget(toolbar)
        btn_add = AddButton()
        btn_add.setToolTip("Add new ingredient.")
        btn_add.clicked.connect(self.addIngredientClicked.emit)
        btn_delete = DeleteButton()
        btn_delete.setToolTip("Delete selected ingredient.")
        btn_delete.clicked.connect(self.deleteIngredientClicked.emit)
        btn_autopopulate = AutopopulateButton()
        btn_autopopulate.setToolTip("Autopopulate ingredient.")
        btn_autopopulate.clicked.connect(self.autopopulateClicked.emit)
        btn_save = SaveJSONButton()
        btn_save.setToolTip("Save ingredient to JSON.")
        btn_save.clicked.connect(self.saveJSONClicked.emit)
        toolbar.addWidget(btn_add)
        toolbar.addWidget(btn_delete)
        toolbar.addWidget(btn_autopopulate)
        toolbar.addWidget(btn_save)

    def _build_search_ui(self, container: QBoxLayout):
        """Build the search UI for the ingredient editor page."""
        self.ingredient_search = SearchColumnView()
        self.ingredient_search.searchTermChanged.connect(self.searchTextChanged.emit)
        self.ingredient_search.searchTermCleared.connect(self.searchTextCleared.emit)
        self.ingredient_search.resultSelected.connect(
            lambda: self.ingredientSelected.emit(
                self.ingredient_search.results_list.selected_item.text() # type: ignore
            )
        )
        container.addWidget(self.ingredient_search)

    def _build_basic_info_UI(self, container: QBoxLayout):
        """Build the UI for the basic info section of the ingredient editor page."""

        # Create the basic info groupbox
        gb_basic_info = QGroupBox("Basic Info")
        container.addWidget(gb_basic_info)

        # Put a vertical layout inside the basic info groubox
        lyt_basic_info = QVBoxLayout()
        gb_basic_info.setLayout(lyt_basic_info)

        # Create a horizontal layout for name and textbox
        lyt_ingredient_name = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_ingredient_name)
        # Create a label and add it to the layout
        label = QLabel("Name:")
        lyt_ingredient_name.addWidget(label)
        # Create a textbox and add it to the layout
        self.txt_ingredient_name = LineEdit()
        # Make the line edit not editable
        self.txt_ingredient_name.setReadOnly(True)
        lyt_ingredient_name.addWidget(self.txt_ingredient_name)
        # Add an edit button
        btn_edit = EditButton()
        lyt_ingredient_name.addWidget(btn_edit)
        btn_edit.clicked.connect(self.editIngredientNameClicked.emit)
        # Reduce the vertical padding in this layout
        lyt_ingredient_name.setContentsMargins(0, 0, 0, 0)

        # Add a description field and multiline textbox
        label = QLabel("Description:")
        lyt_basic_info.addWidget(label)
        self.txt_description = MultilineEdit()
        lyt_basic_info.addWidget(self.txt_description)
        self.txt_description.lostFocus.connect(
            lambda: self.ingredientDescriptionChanged.emit(self.txt_description.toPlainText())
        )

    def _build_cost_UI(self, container: QBoxLayout):
        """Build the UI for the cost section of the ingredient editor page."""
        
        # Create the cost groupbox
        gb_cost = QGroupBox("Cost")
        container.addWidget(gb_cost)

        # Create a horizontal layout for the cost section
        lyt_cost = QHBoxLayout()
        gb_cost.setLayout(lyt_cost)

        # Create the first label
        label = QLabel("Cost: £")
        lyt_cost.addWidget(label)

        # Create a textbox for the cost of the ingredient
        self.txt_cost = NumericLineEdit()
        lyt_cost.addWidget(self.txt_cost)
        self.txt_cost.lostFocus.connect(self.ingredientCostValueChanged.emit)

        # Create a second label
        label = QLabel(" per ")
        lyt_cost.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_cost_quantity = NumericLineEdit()
        lyt_cost.addWidget(self.txt_cost_quantity)
        self.txt_cost_quantity.lostFocus.connect(self.ingredientCostQuantityChanged.emit)

        # Create a units dropdown
        self.cmb_cost_qty_unit = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_cost_qty_unit.addItems(["g", "kg", "ml", "l"])
        lyt_cost.addWidget(self.cmb_cost_qty_unit)
        self.cmb_cost_qty_unit.currentTextChanged.connect(self.ingredientCostQuantityUnitChanged.emit)

    def _build_gi_UI(self, container: QBoxLayout):
        """Build the UI for the GI section of the ingredient editor page."""
        # Create the GI groupbox
        gb_gi = QGroupBox("GI")
        container.addWidget(gb_gi)

        # Put a horizontal layout inside the group box
        column_layout = QHBoxLayout()
        gb_gi.setLayout(column_layout)

        # Create a label and add it to the layout
        label = QLabel("Glycemic Index:")
        column_layout.addWidget(label)

        # Create a line edit and add it to the layout
        self.txt_gi = NumericLineEdit()
        column_layout.addWidget(self.txt_gi)
        self.txt_gi.lostFocus.connect(self.ingredientGIChanged.emit)



