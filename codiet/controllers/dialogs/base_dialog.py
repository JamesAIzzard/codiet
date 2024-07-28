from typing import TypeVar, Generic

from PyQt6.QtWidgets import QWidget

from codiet.views.dialogs.base_dialog_view import BaseDialogView
from codiet.controllers.base_controller import BaseController

T = TypeVar('T', bound=BaseDialogView)

class BaseDialog(BaseController[T], Generic[T]):
    """Base controller class for dialog boxes."""

    def __init__(
            self, 
            title: str|None = None,
            *args, **kwargs
        ):
        super().__init__(
            *args, **kwargs
        )
        if title is not None:
            self.title = title

    @property
    def title(self) -> str:
        """Get the title of the dialog box."""
        return self.view.title
    
    @title.setter
    def title(self, title: str):
        """Set the title of the dialog box."""
        self.view.title = title

    def set_dialog_window_icon(self, icon_name: str):
        """Set the icon for the dialog box frame."""
        self.view.set_dialog_window_icon(icon_name)

    def show(self):
        """Show the dialog box."""
        self.view.exec()

    def close(self):
        """Close the dialog box."""
        self.view.close()

    def _create_view(self, parent: QWidget, *args, **kwargs) -> BaseDialogView:
        return BaseDialogView(parent=parent, *args, **kwargs)