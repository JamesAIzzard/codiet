from typing import Callable

from PyQt6.QtWidgets import QDialog

from codiet.db.database_service import DatabaseService
from codiet.views.ingredient_search_popup_view import IngredientSearchPopupView
from codiet.views.dialog_box_view import ConfirmDialogBoxView

from codiet.models.ingredient import Ingredient

class IngredientSearchPopupCtrl:
    def __init__(
        self,
        view: IngredientSearchPopupView,
        on_result_click: Callable[[Ingredient], None],
    ):
        # Stash the init params
        self.view = view
        self.on_result_click = on_result_click
        # Connect the signals and slots
        self._connect_signals_and_slots()

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

    def on_search_box_text_changed(self, text: str) -> None:
        """Handle the user typing in the search box."""
        with DatabaseService() as db_service:
            # Get the list of matching ingredient names
            matching_names = db_service.fetch_matching_ingredient_names(text)
        # Update the list of matching ingredients
        self.view.update_results_list(matching_names)

    def on_result_clicked(self):
        """Handle the user clicking on a result.
        Loads the ingredient corresponding to the selected result into the
        handler function.
        """
        # Ignore if nothing selected
        if not self.ingredient_is_selected:
            return None
        # Load the ingredient details into the editor
        with DatabaseService() as db_service:
            ingredient = db_service.fetch_ingredient(self.selected_ingredient_name)
        self.on_result_click(ingredient)
        # Close self
        self.view.close()

    def _connect_signals_and_slots(self):
        """Connect the signals and slots."""
        # Connect the search box text changed signal
        self.view.txt_search.textChanged.connect(self.on_search_box_text_changed)
        # Connect the result single click signal
        self.view.lst_search_results.itemClicked.connect(self.on_result_clicked)
