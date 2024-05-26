from typing import Callable

from codiet.views.dialog_box_views import EntityNameDialogView

class EntityNameDialogCtrl:
    """A controller for the entity name dialog."""
    def __init__(
            self, 
            view:EntityNameDialogView,
            check_name_available:Callable[[str], bool],
            on_name_accepted:Callable[[str], None]
    ):
        self.view = view
        self.check_name_available = check_name_available
        self.on_name_accepted = on_name_accepted
        self.view.nameChanged.connect(self._on_name_changed)
        self.view.nameAccepted.connect(on_name_accepted)
        self.view.nameCancelled.connect(self._on_name_edit_cancelled)
        # On initialization, show the instructions, clear the box and disable the OK button
        self.view.show_instructions()
        self.view.clear()
        self.view.disable_ok_button()
        

    def _on_name_changed(self, name: str) -> None:
        """Handler for changes to the name."""
        # If the name is not whitespace
        if self.view.name_is_set:
            # Check if the name is in the cached list of ingredient names
            if not self.check_name_available(name):
                # Show the name unavailable message
                self.view.show_name_unavailable()
                # Disable the OK button
                self.view.disable_ok_button()
            else:
                # Show the name available message
                self.view.show_name_available()
                # Enable the OK button
                self.view.enable_ok_button()
        else:
            # Show the instructions message
            self.view.show_instructions()
            # Disable the OK button
            self.view.disable_ok_button()

    def _on_name_edit_cancelled(self) -> None:
        """Handler for cancelling the new ingredient name."""
        # Clear the new ingredient dialog
        self.view.clear()
        # Hide the new ingredient dialog
        self.view.hide()            