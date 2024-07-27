from PyQt6.QtWidgets import QDialog, QWidget
from PyQt6.QtCore import Qt

from codiet.views import load_icon

class BaseDialogView(QDialog):
    """A base class for dialog boxes with the codiet logo."""
    def __init__(self, title:str = "Title", parent:QWidget|None=None):
        super().__init__(parent=parent)

        # Make the dialog modal
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Set the window title
        self.title = title

        # Set the window icon
        self.set_dialog_window_icon("app-icon.png")

    @property
    def title(self) -> str:
        """Get the title of the dialog box."""
        return self.windowTitle()

    @title.setter
    def title(self, title: str):
        """Set the title of the dialog box."""
        self.setWindowTitle(title)

    def set_dialog_window_icon(self, icon_name: str):
        """Set the icon for the dialog box."""
        self.setWindowIcon(load_icon(icon_name))