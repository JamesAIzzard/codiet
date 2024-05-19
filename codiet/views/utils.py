import os

from codiet.views import STYLESHEETS_DIR

def load_stylesheet(filename:str) -> str:
    """Load the stylesheet for the application."""
    # Build the path
    path = os.path.join(STYLESHEETS_DIR, filename)
    # Read
    with open(path, 'r') as file:
        return file.read()
    