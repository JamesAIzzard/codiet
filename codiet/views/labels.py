from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from codiet.views import load_pixmap_icon

class SearchIconLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        pixmap = load_pixmap_icon('search-icon.png')
        pixmap = pixmap.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(pixmap)