from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QGroupBox,
    QTextEdit,
)
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import pyqtSignal, QVariant

from codiet.views.dialog_box_view import OkDialogBoxView, ConfirmDialogBoxView
from codiet.views.search_views import SearchPopupView
from codiet.views.ingredients_editor_view import IngredientsEditorView
from codiet.views.serve_time_intervals_editor_view import ServeTimeIntervalsEditorView
from codiet.views.recipe_type_editor_view import RecipeTypeEditorView
from codiet.utils.pyqt import block_signals


class RecipeEditorView(QWidget):
    """User interface for editing recipes."""
    # Define signals
    recipeNameChanged = pyqtSignal(str)
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
        # Build the user interface
        self._build_ui()
        # Init the ingredient search popup
        self.ingredient_search_popup = SearchPopupView()


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

    def show_ingredient_search_popop(self) -> None:
        """Show the ingredient search popup."""
        self.ingredient_search_popup.show()

    def show_name_required_popup(self) -> None:
        """Show the name required popup."""
        # Show confirm dialog box
        dialog = OkDialogBoxView(
            message="Please enter a name for the recipe.",
            title="Name Required",
            parent=self,
        )
        _ = dialog.exec()

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

    def on_add_ingredient_clicked(self) -> None:
        """Handle the add ingredient button click."""
        self.show_ingredient_search_popop()

    def _build_ui(self):
        """Build the UI for the recipe editor."""
        # Create a vertical layout for the page
        page_layout = QVBoxLayout()
        self.setLayout(page_layout)

        # Create a label and add it to the layout
        label = QLabel("Recipe Editor")
        font = QFont()
        font.setBold(True)
        label.setFont(font)
        page_layout.addWidget(label)

        # Create a horizontal layout for the columns
        columns_layout = QHBoxLayout()
        page_layout.addLayout(columns_layout)

        # Create the first column
        column1_layout = QVBoxLayout()
        columns_layout.addLayout(column1_layout, 2)

        # Create a 'Basic Info' groupbox
        basic_info_group = QGroupBox("Basic Info")
        column1_layout.addWidget(basic_info_group)
        basic_info_layout = QVBoxLayout()
        basic_info_group.setLayout(basic_info_layout)
        basic_info_layout.setContentsMargins(5, 5, 5, 5)

        # Add a row containg the recipe name label and a textbox
        recipe_name_layout = QHBoxLayout()
        basic_info_layout.addLayout(recipe_name_layout)
        label = QLabel("Name: ")
        recipe_name_layout.addWidget(label)
        self.txt_recipe_name = QLineEdit()
        # Connect to the signal
        self.txt_recipe_name.textChanged.connect(self.recipeNameChanged.emit)
        # Add to the UI
        recipe_name_layout.addWidget(self.txt_recipe_name)

        # Add a row containing the recipe description label and multiline textbox
        label = QLabel("Description:")
        basic_info_layout.addWidget(label)
        self.txt_recipe_description = QTextEdit()
        basic_info_layout.addWidget(self.txt_recipe_description)
        # Make the description box just three lines high
        self.txt_recipe_description.setFixedHeight(60)
        # Connect to the signal, also passing the text
        self.txt_recipe_description.textChanged.connect(
            lambda: self.recipeDescriptionChanged.emit(self.txt_recipe_description.toPlainText())
        )

        # Add a row containing the recipe instructions label and multiline textbox
        label = QLabel("Instructions:")
        basic_info_layout.addWidget(label)
        self.textbox_recipe_instructions = QTextEdit()
        basic_info_layout.addWidget(self.textbox_recipe_instructions)
        # Connect to the signal, also passing the text
        self.textbox_recipe_instructions.textChanged.connect(
            lambda: self.recipeInstructionsChanged.emit(self.textbox_recipe_instructions.toPlainText())
        )

        # Create the second column
        lyt_col_2 = QVBoxLayout()
        columns_layout.addLayout(lyt_col_2, 2)

        # Add the ingredients editor widget to the second col
        self.ingredients_editor = IngredientsEditorView()
        lyt_col_2.addWidget(self.ingredients_editor)
        # Connect the add and remove ingredients editor buttons
        self.ingredients_editor.addIngredientClicked.connect(self.addIngredientClicked.emit)
        self.ingredients_editor.removeIngredientClicked.connect(self.removeIngredientClicked.emit)

        # Create the third column
        lyt_col_3 = QVBoxLayout()
        columns_layout.addLayout(lyt_col_3, 1)

        # Add the serve times editor widget to the third col
        self.serve_time_intervals_editor_view = ServeTimeIntervalsEditorView()
        lyt_col_3.addWidget(self.serve_time_intervals_editor_view)
        # Connect the add and remove serve time buttons
        self.serve_time_intervals_editor_view.addServeTimeClicked.connect(self.addServeTimeClicked.emit)
        self.serve_time_intervals_editor_view.removeServeTimeClicked.connect(self.removeServeTimeClicked.emit)

        # Add the recipe type selector widget to the third col
        self.recipe_type_editor_view = RecipeTypeEditorView()
        lyt_col_3.addWidget(self.recipe_type_editor_view)
        # Connect the add and remove recipe types buttons
        self.recipe_type_editor_view.addRecipeTypeClicked.connect(self.addRecipeTypeClicked.emit)
        self.recipe_type_editor_view.removeRecipeTypeClicked.connect(self.removeRecipeTypeClicked.emit)

        # Add a horizontal layout for the buttons
        lyt_buttons = QHBoxLayout()
        page_layout.addLayout(lyt_buttons)
        # At the bottom of the page, put a 'Save Recipe' button
        self.btn_save_recipe = QPushButton("Save Recipe")
        self.btn_save_recipe.setMaximumWidth(150)
        lyt_buttons.addWidget(self.btn_save_recipe)
        # Connect to the save recipe signal
        self.btn_save_recipe.clicked.connect(self.saveRecipeClicked.emit)
        # Add a 'Save to .json' button
        self.btn_save_json = QPushButton("Save to .json")
        self.btn_save_json.setMaximumWidth(150)
        lyt_buttons.addWidget(self.btn_save_json)
        # Connect to the save to json signal
        self.btn_save_json.clicked.connect(self.saveToJSONClicked.emit)
        # Push the buttons to the left
        lyt_buttons.addStretch()
