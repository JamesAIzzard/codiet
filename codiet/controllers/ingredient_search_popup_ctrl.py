from typing import Callable

from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_search_popup_view import IngredientSearchPopupView

from codiet.models.ingredient import Ingredient

class IngredientSearchPopupCtrl:
    def __init__(
        self,
        view: IngredientSearchPopupView,
        db_service: DatabaseService,
        set_ingredient_instance: Callable[[Ingredient], None],
    ):
        # Stash the init params
        self.view = view
        self.db_service = db_service
        self.set_ingredient_instance = set_ingredient_instance

        # Connect the signals and slots
        self.view.txt_search.textChanged.connect(self.on_search_box_text_changed)
        self.view.btn_select.clicked.connect(self.on_select_clicked)
        self.view.btn_delete.clicked.connect(self.on_delete_clicked)

    @property
    def selected_ingredient_name(self) -> str:
        """Return the name of the selected ingredient."""
        # Get the selected ingredient name
        selected_item = self.view.lst_search_results.currentItem()
        if selected_item is not None:
            return selected_item.text()
        else:
            # Handle the case when no item is selected
            raise ValueError("No ingredient is selected")
        
    @property
    def ingredient_is_selected(self) -> bool:
        """Return True if an ingredient is selected, False otherwise."""
        return self.selected_ingredient_name is not None

    def on_search_box_text_changed(self, text: str):
        """Handle the user typing in the search box."""
        # Get the list of matching ingredient names
        matching_names = self.db_service.load_matching_ingredient_names(text)
        # Update the list of matching ingredients
        self.view.update_ingredient_list(matching_names)

    def on_select_clicked(self):
        """Handle the user clicking the Select button."""
        # Ignore if nothing selected
        if not self.ingredient_is_selected:
            return
        # Load the ingredient details into the editor
        # ingredient = self.db_service.load_ingredient(selected_ingredient_name)
        print(f"TODO: Load {self.selected_ingredient_name}")
        # Close self
        self.view.close()

    def on_delete_clicked(self):
        """Handle the user clicking the Delete button."""
        # Ignore if nothing selected
        if not self.ingredient_is_selected:
            return
        # Delete the ingredient
        self.db_service.delete_ingredient(self.selected_ingredient_name)
        # Update the list of matching ingredients
        self.on_search_box_text_changed(self.view.txt_search.text())
