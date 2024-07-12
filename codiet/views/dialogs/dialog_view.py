from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import Qt

from codiet.views import load_icon

class DialogView(QDialog):
    """A base class for dialog boxes with the codiet logo."""
    def __init__(self, title:str = "Title", parent=None):
        super().__init__(parent=parent)

        # Make the dialog modal
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # Set the window title
        self.setWindowTitle(title)
        # Set the window icon
        self.setWindowIcon(load_icon("app-icon.png"))

    @property
    def title(self):
        return self.windowTitle()

    @title.setter
    def title(self, title: str):
        self.setWindowTitle(title)