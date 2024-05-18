from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class SearchIconLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        pixmap = QPixmap('codiet/resources/icons/search-icon.png')
        # Set the size of the icon
        pixmap = pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(pixmap)