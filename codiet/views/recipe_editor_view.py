from PyQt6.QtWidgets import (
    QWidget,
    QBoxLayout,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QTextEdit,
)
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.views.buttons import EditButton, AddButton, DeleteButton, SaveJSONButton, AutopopulateButton
from codiet.views.dialog_box_views import OkDialogBoxView, ConfirmDialogBoxView
from codiet.views.search_views import SearchColumnView
from codiet.views.ingredients_editor_view import IngredientsEditorView
from codiet.views.serve_time_intervals_editor_view import ServeTimeIntervalsEditorView
from codiet.views.recipe_type_editor_view import RecipeTypeEditorView
from codiet.utils.pyqt import block_signals


class RecipeEditorView(QWidget):
    """User interface for editing recipes."""
    # Define signals
    addRecipeClicked = pyqtSignal()
    deleteRecipeClicked = pyqtSignal()
    autopopulateRecipeClicked = pyqtSignal()
    saveJSONClicked = pyqtSignal()
    searchTextChanged = pyqtSignal(str)
    searchTextCleared = pyqtSignal()
    recipeSelected = pyqtSignal(QVariant)
    editRecipeNameClicked = pyqtSignal()
    recipeDescriptionChanged = pyqtSignal(str)
    recipeInstructionsChanged = pyqtSignal(str)
    addIngredientClicked = pyqtSignal()
    removeIngredientClicked = pyqtSignal()
    addServeTimeClicked = pyqtSignal()
    removeServeTimeClicked = pyqtSignal()
    addRecipeTypeClicked = pyqtSignal()
    removeRecipeTypeClicked = pyqtSignal()
    saveRecipeClicked = pyqtSignal()
    saveToJSONClicked = pyqtSignal()


    def __init__(self):
        super().__init__()
        self._build_ui()

    def update_name(self, name: str | None) -> None:
        """Set the recipe name."""
        with block_signals(self.txt_recipe_name):
            if name is None:
                self.txt_recipe_name.clear()
            elif name.strip() == "":
                self.txt_recipe_name.clear()
            else:
                self.txt_recipe_name.setText(name)

    def update_description(self, description: str | None) -> None:
        """Set the recipe description."""
        with block_signals(self.txt_recipe_description):
            if description is None:
                self.txt_recipe_description.clear()
            elif description.strip() == "":
                self.txt_recipe_description.clear()
            else:
                self.txt_recipe_description.setPlainText(description)

    def update_instructions(self, instructions: str | None) -> None:
        """Update the recipe instructions."""
        with block_signals(self.textbox_recipe_instructions):
            if instructions is None:
                self.textbox_recipe_instructions.clear()
            elif instructions.strip() == "":
                self.textbox_recipe_instructions.clear()
            else:
                self.textbox_recipe_instructions.setPlainText(instructions)

    def update_recipe_types(self, recipe_types: list[str]) -> None:
        """Update the recipe types."""
        self.recipe_type_editor_view.update_recipe_types(recipe_types)

    def show_name_change_confirmation_popup(self) -> bool:
        """Show the name change confirmation popup."""
        # Show confirm dialog box
        dialog = ConfirmDialogBoxView(
            message="Recipe name has changed. Are you sure you want to update the name?",
            title="Recipe Name Change",
            parent=self,
        )
        return dialog.exec() == QDialog.DialogCode.Accepted

    def show_save_confirmation_popup(self) -> None:
        """Show the save confirmation popup."""
        # Show confirm dialog box
        dialog = OkDialogBoxView(
            message="Recipe saved.",
            title="Recipe Saved",
            parent=self,
        )
        _ = dialog.exec()

    def show_update_confirmation_popup(self) -> None:    
        """Show the update confirmation popup."""
        # Show confirm dialog box
        dialog = OkDialogBoxView(
            message="Recipe updated.",
            title="Recipe updated",
            parent=self,
        )
        _ = dialog.exec()

    def _build_ui(self):
        """Build the UI for the recipe editor."""
        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)

        # Create a horizontal layout for the columns
        lyt_top_level_columns = QHBoxLayout()
        page_layout.addLayout(lyt_top_level_columns)

        # Create the search column
        lyt_search_column = QVBoxLayout()
        lyt_top_level_columns.addLayout(lyt_search_column, 1)
        lyt_search_column.setContentsMargins(0, 0, 0, 0)
        self._build_search_ui(lyt_search_column)

        # Create the basic info column
        lyt_basic_info_column = QVBoxLayout()
        lyt_top_level_columns.addLayout(lyt_basic_info_column, 2)
        lyt_search_column.setContentsMargins(0, 0, 0, 0)
        self._build_basic_info_ui(lyt_basic_info_column)

        # Create the ingredients column
        lyt_ingredients_column = QVBoxLayout()
        lyt_top_level_columns.addLayout(lyt_ingredients_column, 2)
        lyt_ingredients_column.setContentsMargins(0, 0, 0, 0)
        self._build_ingredients_ui(lyt_ingredients_column)

        # Create the times and types column
        lyt_times_and_types_column = QVBoxLayout()
        lyt_top_level_columns.addLayout(lyt_times_and_types_column, 2)
        lyt_times_and_types_column.setContentsMargins(0, 0, 0, 0)
        self._build_times_and_types_ui(lyt_times_and_types_column)

    def _build_search_ui(self, container: QBoxLayout) -> None:
        """Build the search UI."""
        # Add a horizontal row for buttons
        lyt_buttons = QHBoxLayout()
        lyt_buttons.setContentsMargins(0, 0, 0, 0)
        container.addLayout(lyt_buttons)
        # Add an add, remove and save to json button.
        btn_add = AddButton()
        btn_add.clicked.connect(self.addRecipeClicked.emit)
        btn_delete = DeleteButton()
        btn_delete.clicked.connect(self.deleteRecipeClicked.emit)
        btn_autopopulate = AutopopulateButton()
        btn_autopopulate.clicked.connect(self.autopopulateRecipeClicked.emit)
        btn_save = SaveJSONButton()
        btn_save.clicked.connect(self.saveJSONClicked.emit)
        lyt_buttons.addWidget(btn_add)
        lyt_buttons.addWidget(btn_delete)
        lyt_buttons.addWidget(btn_autopopulate)
        lyt_buttons.addWidget(btn_save)
        # Push buttons to left
        lyt_buttons.addStretch()
        # Add a search widget
        self.recipe_search = SearchColumnView()
        self.recipe_search.searchTermChanged.connect(self.searchTextChanged.emit)
        self.recipe_search.searchTermCleared.connect(self.searchTextCleared.emit)
        self.recipe_search.resultSelected.connect(self.recipeSelected.emit)
        container.addWidget(self.recipe_search)

    def _build_basic_info_ui(self, container: QBoxLayout) -> None:
        """Builds the basic info UI."""
        # Create a 'Basic Info' groupbox
        grp_basic_info = QGroupBox("Basic Info")
        container.addWidget(grp_basic_info)
        lyt_basic_info = QVBoxLayout()
        grp_basic_info.setLayout(lyt_basic_info)
        lyt_basic_info.setContentsMargins(5, 5, 5, 5)

        # Create a horizontal layout for name and textbox
        lyt_recipe_name = QHBoxLayout()
        lyt_basic_info.addLayout(lyt_recipe_name)
        # Create a label and add it to the layout
        label = QLabel("Name:")
        lyt_recipe_name.addWidget(label)
        # Create a textbox and add it to the layout
        self.txt_recipe_name = QLineEdit()
        # Make the line edit not editable
        self.txt_recipe_name.setReadOnly(True)
        lyt_recipe_name.addWidget(self.txt_recipe_name)
        # Add an edit button
        btn_edit = EditButton()
        lyt_recipe_name.addWidget(btn_edit)
        btn_edit.clicked.connect(self.editRecipeNameClicked.emit)
        # Reduce the vertical padding in this layout
        lyt_recipe_name.setContentsMargins(0, 0, 0, 0)

        # Add a row containing the recipe description label and multiline textbox
        label = QLabel("Description:")
        lyt_basic_info.addWidget(label)
        self.txt_recipe_description = QTextEdit()
        lyt_basic_info.addWidget(self.txt_recipe_description)
        # Make the description box just three lines high
        self.txt_recipe_description.setFixedHeight(60)
        # Connect to the signal, also passing the text
        self.txt_recipe_description.textChanged.connect(
            lambda: self.recipeDescriptionChanged.emit(self.txt_recipe_description.toPlainText())
        )

        # Add a row containing the recipe instructions label and multiline textbox
        label = QLabel("Instructions:")
        lyt_basic_info.addWidget(label)
        self.textbox_recipe_instructions = QTextEdit()
        lyt_basic_info.addWidget(self.textbox_recipe_instructions)
        # Connect to the signal, also passing the text
        self.textbox_recipe_instructions.textChanged.connect(
            lambda: self.recipeInstructionsChanged.emit(self.textbox_recipe_instructions.toPlainText())
        )

    def _build_ingredients_ui(self, container: QBoxLayout) -> None:
        """Build the ingredients UI."""
        # Add the ingredients editor widget to the second col
        self.ingredients_editor = IngredientsEditorView()
        container.addWidget(self.ingredients_editor)
        # Connect the add and remove ingredients editor buttons
        self.ingredients_editor.addIngredientClicked.connect(self.addIngredientClicked.emit)
        self.ingredients_editor.removeIngredientClicked.connect(self.removeIngredientClicked.emit)

    def _build_times_and_types_ui(self, container: QBoxLayout) -> None:
        """Build the times and types UI."""
        # Add the serve times editor widget to the third col
        self.serve_time_intervals_editor_view = ServeTimeIntervalsEditorView()
        container.addWidget(self.serve_time_intervals_editor_view)
        # Connect the add and remove serve time buttons
        self.serve_time_intervals_editor_view.addServeTimeClicked.connect(self.addServeTimeClicked.emit)
        self.serve_time_intervals_editor_view.removeServeTimeClicked.connect(self.removeServeTimeClicked.emit)

        # Add the recipe type selector widget to the third col
        self.recipe_type_editor_view = RecipeTypeEditorView()
        container.addWidget(self.recipe_type_editor_view)
        # Connect the add and remove recipe types buttons
        self.recipe_type_editor_view.addRecipeTypeClicked.connect(self.addRecipeTypeClicked.emit)
        self.recipe_type_editor_view.removeRecipeTypeClicked.connect(self.removeRecipeTypeClicked.emit)