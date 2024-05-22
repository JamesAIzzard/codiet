from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from codiet.views import load_pixmap_icon

class IconLabel(QWidget):
    """A QWidget containing an icon and a text label."""
    def __init__(self, icon_filename: str, icon_size:int=20, text: str|None=None, parent=None):
        super().__init__(parent)
        # Add a top level layout for the icon and text
        self.lyt_top_level = QHBoxLayout(self)
        # Create the icon and text
        self.icon_label = QLabel(self)
        self.text_label = QLabel(self)
        self.lyt_top_level.addWidget(self.icon_label)
        self.lyt_top_level.addWidget(self.text_label)
        # Push to LHS
        self.lyt_top_level.addStretch(1)
        # Set the initial values
        self.set_icon(icon_filename)
        self.set_icon_size(icon_size)
        if text is not None:
            self.set_text(text)

    def set_icon(self, icon_filename: str) -> None:
        """Set the icon of the label."""
        pixmap = load_pixmap_icon(icon_filename)
        self.icon_label.setPixmap(pixmap)

    def set_icon_size(self, height: int) -> None:
        """Set the size of the icon."""
        pixmap = self.icon_label.pixmap().scaled(height, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon_label.setPixmap(pixmap)

    def set_text(self, text: str) -> None:
        """Set the text of the label."""
        self.text_label.setText(text)

class SearchIconLabel(IconLabel):
    """A QLabel with a search icon."""
    def __init__(self, parent=None):
        super().__init__('search-icon.png', parent=parent)