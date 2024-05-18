from PyQt6.QtWidgets import (
    QWidget,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox,
    QLineEdit,
    QTextEdit,
    QComboBox
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.utils.pyqt import block_signals
from codiet.views.buttons import SaveButton
from codiet.views.custom_line_editors import NumericLineEdit
from codiet.views.flag_editor_view import FlagEditorView
from codiet.views.ingredient_nutrients_editor_view import IngredientNutrientsEditorView


class IngredientEditorView(QWidget):
    """User interface for editing an ingredient."""
    # Define signals
    ingredientNameChanged = pyqtSignal(str)
    ingredientDescriptionChanged = pyqtSignal(str)
    ingredientCostValueChanged = pyqtSignal(QVariant)
    ingredientCostQuantityChanged = pyqtSignal(QVariant)
    ingredientCostQuantityUnitChanged = pyqtSignal(str)
    ingredientDensityVolChanged = pyqtSignal(QVariant)
    ingredientDensityVolUnitChanged = pyqtSignal(str)
    ingredientDensityMassChanged = pyqtSignal(QVariant)
    ingredientDensityMassUnitChanged = pyqtSignal(str)
    ingredientNumPiecesChanged = pyqtSignal(QVariant)
    ingredientPieceMassChanged = pyqtSignal(QVariant)
    ingredientPieceMassUnitChanged = pyqtSignal(str)
    ingredientGIChanged = pyqtSignal(QVariant)
    saveIngredientClicked = pyqtSignal()


    def __init__(self):
        super().__init__()

        # Build the UI
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

    def update_density_vol_value(self, density_vol: float | None):
        """Set the density volume value."""
        with block_signals(self.txt_dens_vol):
            if density_vol is not None:
                self.txt_dens_vol.setText(density_vol)
            else:
                self.txt_dens_vol.clear()

    def update_density_vol_unit(self, density_vol_unit: str):
        """Set the density volume unit."""
        with block_signals(self.cmb_dens_vol_unit):
            self.cmb_dens_vol_unit.setCurrentText(density_vol_unit)

    def update_density_mass_value(self, density_mass: float | None):
        """Set the density mass value."""
        with block_signals(self.txt_dens_mass):
            if density_mass is not None:
                self.txt_dens_mass.setText(density_mass)
            else:
                self.txt_dens_mass.clear()

    def update_density_mass_unit(self, density_mass_unit: str):
        """Set the density mass unit."""
        with block_signals(self.cmb_dens_mass_unit):
            self.cmb_dens_mass_unit.setCurrentText(density_mass_unit)

    def update_pc_qty_value(self, num_pieces: float | None):
        """Set the number of pieces value."""
        with block_signals(self.txt_num_pieces):
            if num_pieces is not None:
                self.txt_num_pieces.setText(num_pieces)
            else:
                self.txt_num_pieces.clear()

    def update_pc_mass_value(self, piece_mass: float | None):
        """Set the piece mass value."""
        with block_signals(self.txt_pc_mass_value):
            if piece_mass is not None:
                self.txt_pc_mass_value.setText(piece_mass)
            else:
                self.txt_pc_mass_value.clear()

    def update_pc_mass_unit(self, piece_mass_unit: str):
        """Set the piece mass unit."""
        with block_signals(self.cmb_pc_mass_unit):
            self.cmb_pc_mass_unit.setCurrentText(piece_mass_unit)

    def update_gi(self, gi: float | None):
        """Set the GI value in the GI textbox."""
        with block_signals(self.txt_gi):
            if gi is None:
                self.txt_gi.clear()
            else:
                self.txt_gi.setText(gi)

    def _build_ui(self):
        """Build the UI for the ingredient editor page."""
        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        # Set the layout for the page
        self.setLayout(page_layout)

        # Create a label and add it to the page layout
        label = QLabel("Ingredient Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        page_layout.addWidget(label)

        # Create a horizontal layout for the columns
        columns_layout = QHBoxLayout()
        page_layout.addLayout(columns_layout)

        # Create a vertical layout for the first column
        column1_layout = QVBoxLayout()
        columns_layout.addLayout(column1_layout, 1)

        # Add the basic info section to the column 1 layout
        self._build_basic_info_UI(column1_layout)

        # Add the cost editor to the column 1 layout
        self._build_cost_UI(column1_layout)

        # Add the bulk properties widget to the column1 layout
        self._build_bulk_properties_UI(column1_layout)

        # Add the flags widget to the column1 layout
        self.flag_editor = FlagEditorView()
        column1_layout.addWidget(self.flag_editor)

        # Add the GI widget to the column1 layout
        self._build_gi_UI(column1_layout)

        # Add stretch to end of layout
        column1_layout.addStretch(1)

        # Create the second column.
        lyt_col_2 = QVBoxLayout()
        columns_layout.addLayout(lyt_col_2, 1)

        # Create a nutrient editor widget and add it to the column2 layout
        self.nutrient_editor = IngredientNutrientsEditorView()
        lyt_col_2.addWidget(self.nutrient_editor)

        # Add a save ingredient button to the bottom of the page
        self.btn_save_ingredient = SaveButton()
        page_layout.addWidget(self.btn_save_ingredient)

    def _build_basic_info_UI(self, container: QBoxLayout):
        """Build the UI for the basic info section of the ingredient editor page."""

        # Create the basic info groupbox
        gb_basic_info = QGroupBox("Basic Info")
        container.addWidget(gb_basic_info)

        # Put a vertical layout inside the basic info groubox
        lyt_top_level = QVBoxLayout()
        gb_basic_info.setLayout(lyt_top_level)

        # Create a horizontal layout for name and textbox
        lyt_ingredient_name = QHBoxLayout()
        lyt_top_level.addLayout(lyt_ingredient_name)

        # Create a label and add it to the layout
        label = QLabel("Name:")
        lyt_ingredient_name.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_ingredient_name = QLineEdit()
        lyt_ingredient_name.addWidget(self.txt_ingredient_name)
        self.txt_ingredient_name.textChanged.connect(self.ingredientNameChanged.emit)

        # Reduce the vertical padding in this layout
        lyt_ingredient_name.setContentsMargins(0, 0, 0, 0)

        # Add a description field and multiline textbox
        label = QLabel("Description:")
        lyt_top_level.addWidget(label)
        self.txt_description = QTextEdit()
        lyt_top_level.addWidget(self.txt_description)
        self.txt_description.textChanged.connect(
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
        self.txt_cost.valueChanged.connect(self.ingredientCostValueChanged.emit)

        # Create a second label
        label = QLabel(" per ")
        lyt_cost.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_cost_quantity = NumericLineEdit()
        lyt_cost.addWidget(self.txt_cost_quantity)
        self.txt_cost_quantity.valueChanged.connect(self.ingredientCostQuantityChanged.emit)

        # Create a units dropdown
        self.cmb_cost_qty_unit = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_cost_qty_unit.addItems(["g", "kg", "ml", "l"])
        lyt_cost.addWidget(self.cmb_cost_qty_unit)
        self.cmb_cost_qty_unit.currentTextChanged.connect(self.ingredientCostQuantityUnitChanged.emit)

    def _build_bulk_properties_UI(self, container: QBoxLayout):
        """Build the UI for the bulk properties section of the ingredient editor page."""
        # Create the bulk properties groupbox
        gb_bulk_properties = QGroupBox("Bulk Properties")
        container.addWidget(gb_bulk_properties)

        # Add a vertical layout inside the groubox
        lyt_top_level = QVBoxLayout()
        gb_bulk_properties.setLayout(lyt_top_level)

        # Add a horizontal layout for the density editor
        lyt_density = QHBoxLayout()
        lyt_top_level.addLayout(lyt_density)

        # Create a label and add it to the layout
        label = QLabel("Density:")
        lyt_density.addWidget(label)

        # Create the density volume textbox and add it to the layout
        self.txt_dens_vol = NumericLineEdit()
        lyt_density.addWidget(self.txt_dens_vol)
        self.txt_dens_vol.valueChanged.connect(self.ingredientDensityVolChanged.emit)

        # Create a density volume units dropdown and add it to the layout
        self.cmb_dens_vol_unit = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_dens_vol_unit.addItems(["ml", "l"])
        lyt_density.addWidget(self.cmb_dens_vol_unit)
        self.cmb_dens_vol_unit.currentTextChanged.connect(self.ingredientDensityVolUnitChanged.emit)

        # Create another label and add it to the layout
        label = QLabel(" weighs ")
        lyt_density.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_dens_mass = NumericLineEdit()
        lyt_density.addWidget(self.txt_dens_mass)
        self.txt_dens_mass.valueChanged.connect(self.ingredientDensityMassChanged.emit)

        # Create a mass units dropdown and add it to the layout
        self.cmb_dens_mass_unit = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_dens_mass_unit.addItems(["g", "kg"])
        lyt_density.addWidget(self.cmb_dens_mass_unit)
        self.cmb_dens_mass_unit.currentTextChanged.connect(self.ingredientDensityMassUnitChanged.emit)
        
        # Add a horizontal layout for the piece mass editor
        lyt_piece_mass = QHBoxLayout()
        lyt_top_level.addLayout(lyt_piece_mass)

        # Create a label and add it to the layout
        label = QLabel("Piece Mass:")
        lyt_piece_mass.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_num_pieces = NumericLineEdit()
        lyt_piece_mass.addWidget(self.txt_num_pieces)
        self.txt_num_pieces.valueChanged.connect(self.ingredientNumPiecesChanged.emit)

        # Create another label
        label = QLabel(" piece(s) weighs ")
        lyt_piece_mass.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_pc_mass_value = NumericLineEdit()
        lyt_piece_mass.addWidget(self.txt_pc_mass_value)
        self.txt_pc_mass_value.valueChanged.connect(self.ingredientPieceMassChanged.emit)

        # Create a mass units dropdown and add it to the layout
        self.cmb_pc_mass_unit = QComboBox()
        # Temporarily add units, these will get pulled from config file later
        # TODO - pull units from config file
        self.cmb_pc_mass_unit.addItems(["g", "kg"])
        lyt_piece_mass.addWidget(self.cmb_pc_mass_unit)
        self.cmb_pc_mass_unit.currentTextChanged.connect(self.ingredientPieceMassUnitChanged.emit)

    def _build_gi_UI(self, container: QBoxLayout):
        """Build the UI for the GI section of the ingredient editor page."""
        # Create the GI groupbox
        gb_gi = QGroupBox("GI")
        container.addWidget(gb_gi)

        # Put a horizontal layout inside the group box
        column_layout = QHBoxLayout()
        gb_gi.setLayout(column_layout)

        # Create a label and add it to the layout
        label = QLabel("Glycemic Index (Carbohydrate Only):")
        column_layout.addWidget(label)

        # Create a line edit and add it to the layout
        self.txt_gi = NumericLineEdit()
        column_layout.addWidget(self.txt_gi)
        self.txt_gi.valueChanged.connect(self.ingredientGIChanged.emit)

