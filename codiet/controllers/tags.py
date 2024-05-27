from typing import Callable

from codiet.db.database_service import DatabaseService
from codiet.views.dialog_box_views import OkDialogBoxView
from codiet.views.tags import RecipeTagEditorView, RecipeTagSelectorPopup
from codiet.controllers.search import SearchColumnCtrl

class RecipeTagEditorCtrl():
    """Controller for the recipe tag editor view."""
    def __init__(self,
            recipe_tag_editor_view: RecipeTagEditorView,
            recipe_tag_selector_popup: RecipeTagSelectorPopup,
            on_tag_added: Callable[[str], None],
            on_tag_removed: Callable[[str], None]
        ):
        self.recipe_tag_editor_view = recipe_tag_editor_view
        self.recipe_tag_selector_popup = recipe_tag_selector_popup
        self.on_tag_added = on_tag_added
        self.on_tag_removed = on_tag_removed

        # Cache the global recipe tags
        self._recipe_tags:list[str] = []
        self._cache_recipe_tags()

        # Add the controller for the search column
        tag_search_ctrl = SearchColumnCtrl(
            view=self.recipe_tag_selector_popup.search_column,
            get_data=lambda: self._recipe_tags,
            on_result_selected=self._on_tag_selected,
        )

        # Connect signals
        self.recipe_tag_editor_view.addRecipeTagClicked.connect(self._on_add_recipe_tag_clicked)
        self.recipe_tag_editor_view.removeRecipeTagClicked.connect(self._on_remove_recipe_tag_clicked)

    def update_recipe_tags(self, tags:list[str]) -> None:
        """Update the recipe tags in the editor."""
        self.recipe_tag_editor_view.clear_tags()
        for tag in tags:
            self.recipe_tag_editor_view.add_tag(tag)

    def _cache_recipe_tags(self) -> None:
        """Cache the global recipe tags."""
        with DatabaseService() as db_service:
            self._recipe_tags = db_service.fetch_all_global_recipe_tags()

    def _on_add_recipe_tag_clicked(self) -> None:
        """Handle the add recipe tag button clicked event."""
        self._cache_recipe_tags()
        self.recipe_tag_selector_popup.show()

    def _on_remove_recipe_tag_clicked(self, tag: str|None) -> None:
        """Handle the remove recipe tag button clicked event."""
        # If there is no tag selected
        if tag is None:
            # Open info popup to tell user to select tag.
            dialog = OkDialogBoxView(
                parent=self.recipe_tag_editor_view,
                title="No Tag Selected",
                message="Please select a tag to remove.",
            )
            dialog.okClicked.connect(dialog.close)
            dialog.show()
        else:
            # Handle the updates to the widget
            self.recipe_tag_editor_view.remove_tag(tag)
            # Call the callback
            self.on_tag_removed(tag)

    def _on_tag_selected(self, tag: str) -> None:
        """Handle the result selected event."""
        # Handle the updates to the widget
        self.recipe_tag_editor_view.add_tag(tag)
        # Call the callback
        self.on_tag_added(tag)