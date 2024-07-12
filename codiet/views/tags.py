from PyQt6.QtCore import pyqtSignal, QVariant
from PyQt6.QtWidgets import (
    QSizePolicy,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QListWidget,
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QListWidget,
)

from codiet.views.buttons import AddButton, RemoveButton
from codiet.views.dialogs import DialogBoxView
from codiet.views.search import SearchColumnView

class RecipeTagEditorView(QWidget):
    # Define signals
    addRecipeTagClicked = pyqtSignal()
    removeRecipeTagClicked = pyqtSignal(QVariant)
    recipeTagSelected = pyqtSignal(str)
    tagSearchChanged = pyqtSignal(str)
    tagSearchCleared = pyqtSignal()


    """UI element to allow the user to select/deselect recipe tags."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()

    @property
    def selected_index(self) -> int:
        """Get the index of the selected recipe tag."""
        return self.lst_recipe_tags.currentRow()
    
    @property
    def tag_is_selected(self) -> bool:
        """Check if a recipe tag is selected."""
        return self.selected_index != -1
    
    @property
    def selected_tag(self) -> str|None:
        """Get the selected recipe tag."""
        if self.tag_is_selected:
            return self.lst_recipe_tags.currentItem().text() # type: ignore
        else:
            return None

    def add_tag(self, tag: str) -> None:
        """Add a tag to the list of recipe tags."""
        self.lst_recipe_tags.addItem(tag)

    def remove_tag(self, tag:str) -> None:
        """Remove a tag from the list of recipe tags."""
        # Find the index of the tag
        for index in range(self.lst_recipe_tags.count()):
            if self.lst_recipe_tags.item(index).text() == tag: # type: ignore
                self.lst_recipe_tags.takeItem(index)
                break

    def clear_tags(self) -> None:
        """Clear all tags from the list of recipe tags."""
        self.lst_recipe_tags.clear()

    def _build_ui(self):
        """Build the UI for the recipe tag editor."""
        # Create a vertical layout for the page
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Remove all margins
        lyt_top_level.setContentsMargins(0, 0, 0, 0)

        # Add a groupbox for the recipe tags
        gb_recipe_tags = QGroupBox("Recipe Tags")
        lyt_top_level.addWidget(gb_recipe_tags)
        lyt_recipe_tags = QVBoxLayout()
        gb_recipe_tags.setLayout(lyt_recipe_tags)
        lyt_recipe_tags.setContentsMargins(5, 5, 5, 5)

        lyt_buttons = QHBoxLayout()
        lyt_recipe_tags.addLayout(lyt_buttons)
        btn_add_tag = AddButton()
        btn_remove_tag = RemoveButton()
        lyt_buttons.addWidget(btn_add_tag)
        lyt_buttons.addWidget(btn_remove_tag)
        btn_add_tag.clicked.connect(self.addRecipeTagClicked.emit)
        btn_remove_tag.clicked.connect(
            lambda: self.removeRecipeTagClicked.emit(self.selected_tag)
        )
        # Push buttons to LHS
        lyt_buttons.addStretch()

        # Add a listbox for the recipe tags
        self.lst_recipe_tags = QListWidget()
        lyt_recipe_tags.addWidget(self.lst_recipe_tags)
        self.lst_recipe_tags.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

class RecipeTagSelectorPopup(DialogBoxView):
    # Define signals
    tagSearchChanged = pyqtSignal(str)
    tagSearchCleared = pyqtSignal()
    
    def __init__(self, *args, **kwargs):
        super().__init__(title="Recipe Tags", *args, **kwargs)
        self.setWindowTitle("Select Recipe Tags")
        self._build_ui()

    def _build_ui(self) -> None:
        """Build the UI for the recipe tag selector popup."""
        # Create a vertical layout for the page
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)

        # Add a search column
        self.search_column = SearchColumnView()
        lyt_top_level.addWidget(self.search_column)
