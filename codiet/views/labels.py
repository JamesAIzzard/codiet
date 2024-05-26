from PyQt6.QtWidgets import QLabel, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from codiet.views import load_pixmap_icon

class IconLabel(QLabel):
    """A QLabel with an icon."""
    def __init__(self, icon_filename: str, icon_size:int=20, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_icon(icon_filename)
        self.set_icon_size(icon_size)

    def set_icon(self, icon_filename: str) -> None:
        """Set the icon of the label."""
        pixmap = load_pixmap_icon(icon_filename)
        self.setPixmap(pixmap)

    def set_icon_size(self, height: int) -> None:
        """Set the size of the icon."""
        pixmap = self.pixmap().scaled(height, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(pixmap)

class IconTextLabel(QWidget):
    """A QWidget containing an icon and a text label."""
    def __init__(self, icon_filename: str, icon_size:int=20, text: str|None=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add a top level layout for the icon and text
        self.lyt_top_level = QHBoxLayout(self)
        # Create the icon and text
        self.lbl_icon = IconLabel(icon_filename, icon_size, self)
        self.txt_label = QLabel(self)
        self.lyt_top_level.addWidget(self.lbl_icon)
        self.lyt_top_level.addWidget(self.txt_label)
        # Push to LHS
        self.lyt_top_level.addStretch(1)
        # Set the initial values
        self.set_icon(icon_filename)
        self.set_icon_size(icon_size)
        if text is not None:
            self.text = text

    @property
    def text(self) -> str:
        """Return the text of the label."""
        return self.txt_label.text()
    
    @text.setter
    def text(self, text: str) -> None:
        """Set the text of the label."""
        self.txt_label.setText(text)

    def set_icon(self, icon_filename: str) -> None:
        """Set the icon of the label."""
        self.lbl_icon.set_icon(icon_filename)

    def set_icon_size(self, height: int) -> None:
        """Set the size of the icon."""
        self.lbl_icon.set_icon_size(height)

class SearchIconLabel(IconLabel):
    """A QLabel with a search icon."""
    def __init__(self, parent=None):
        super().__init__(icon_filename='search-icon.png', parent=parent)