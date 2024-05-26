import os

from PyQt6.QtGui import QIcon, QPixmap

STYLESHEETS_DIR = os.path.join('codiet', 'views', 'styles')
ICONS_DIR = os.path.join('codiet', 'views', 'resources', 'icons')

def load_stylesheet(filename:str) -> str:
    """Load the stylesheet for the application."""
    # Build the path
    path = os.path.join(STYLESHEETS_DIR, filename)
    # Read
    with open(path, 'r') as file:
        return file.read()

def load_icon(icon_filename: str) -> QIcon:
    """Load an icon from the resources directory."""
    # Create the filepath
    icon_filepath = os.path.join(ICONS_DIR, icon_filename)
    # Raise an exception if the icon does not exist
    if not os.path.exists(icon_filepath):
        raise FileNotFoundError(f"Icon {icon_filename} not found at {icon_filepath}.")
    return QIcon(os.path.join(ICONS_DIR, icon_filename))

def load_pixmap_icon(icon_filename: str) -> QPixmap:
    """Load a pixmap from the resources directory."""
    # Create the filepath
    icon_filepath = os.path.join(ICONS_DIR, icon_filename)
    # Raise an exception if the icon does not exist
    if not os.path.exists(icon_filepath):
        raise FileNotFoundError(f"Icon {icon_filename} not found at {icon_filepath}.")
    return QPixmap(os.path.join(ICONS_DIR, icon_filename))