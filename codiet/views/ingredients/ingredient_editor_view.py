from PyQt6.QtWidgets import (
    QWidget,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QGroupBox
)

from codiet.views.icon_button import IconButton
from codiet.views.text_editors.line_editor import LineEditor
from codiet.views.text_editors.multiline_editor import MultilineEditor
from codiet.views.text_editors.numeric_line_editor import NumericLineEditor
from codiet.views.editor_toolbar import EditorToolbar
from codiet.views.search.search_column_view import SearchColumnView
from codiet.views.entity_name_editor_view import EntityNameEditorView
from codiet.views.cost_editor_view import CostEditorView
from codiet.views.nutrients.nutrient_quantities_editor_view import NutrientQuantitiesEditorView
from codiet.views.flags.flag_editor_view import FlagEditorView
from codiet.views.units.standard_unit_editor_view import StandardUnitEditorView
from codiet.views.units.unit_conversions_editor_view import UnitConversionsEditorView

class IngredientEditorView(QWidget):
    """User interface for editing an ingredient."""

    def __init__(self, *args, **kwargs):
        """Initialise the ingredient editor view."""
        super().__init__(*args, **kwargs)

        self._build_ui()

    def _build_ui(self):
        """Build the UI for the ingredient editor page."""
        # Create a top level layout
        lyt_top_level = QVBoxLayout()
        lyt_top_level.setContentsMargins(0, 0, 0, 0)
        self.setLayout(lyt_top_level)

        # Put the toolbar in it
        self.toolbar = EditorToolbar(entity_name="ingredient")
        lyt_top_level.addWidget(self.toolbar)

        # Create a horizontal layout for the columns
        lyt_columns = QHBoxLayout()
        lyt_columns.setContentsMargins(5, 5, 5, 5)
        lyt_top_level.addLayout(lyt_columns)

        # Create the ingredient search column
        lyt_search_column = QVBoxLayout()
        lyt_columns.addLayout(lyt_search_column, 1)        
        self.ingredient_search_column = SearchColumnView()
        lyt_search_column.addWidget(self.ingredient_search_column)
        lyt_search_column.setContentsMargins(0, 0, 0, 0)

        # Create a col for the basic info, cost, flags and GI
        lyt_first_col = QVBoxLayout()
        lyt_columns.addLayout(lyt_first_col, 1)
        self._build_basic_info_UI(lyt_first_col)
        # Add the standard unit editor
        self.standard_unit_editor = StandardUnitEditorView()
        # Add the measurement definition view
        self.unit_conversions_editor = UnitConversionsEditorView()
        lyt_first_col.addWidget(self.unit_conversions_editor)        
        # Add the cost editor to the column 1 layout
        self.cost_editor = CostEditorView()
        lyt_first_col.addWidget(self.cost_editor)
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

    def _build_basic_info_UI(self, container: QBoxLayout):
        """Build the UI for the basic info section of the ingredient editor page."""

        # Create the basic info groupbox
        gb_basic_info = QGroupBox("Basic Info")
        container.addWidget(gb_basic_info)

        # Put a vertical layout inside the basic info groubox
        lyt_basic_info = QVBoxLayout()
        gb_basic_info.setLayout(lyt_basic_info)

        # Create a horizontal layout for name and textbox
        self.name_editor_view = EntityNameEditorView(parent=self)
        lyt_basic_info.addWidget(self.name_editor_view)

        # Add a description field and multiline textbox
        label = QLabel("Description:")
        lyt_basic_info.addWidget(label)
        self.txt_description = MultilineEditor()
        lyt_basic_info.addWidget(self.txt_description)
        self.txt_description.lostFocus.connect(
            lambda: self.ingredientDescriptionChanged.emit(self.txt_description.toPlainText())
        )
        
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
        self.txt_gi = NumericLineEditor()
        column_layout.addWidget(self.txt_gi)
        # self.txt_gi.lostFocus.connect(self.ingredientGIChanged.emit)



