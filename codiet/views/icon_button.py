from PyQt6.QtWidgets import QPushButton,QSizePolicy

from codiet.views import load_icon

class IconButton(QPushButton):
    def __init__(self, icon_filename:str, text:str|None=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the icon
        self.setIcon(load_icon(icon_filename))
        # If the text is set, set it
        if text is not None:
            self.setText(text)
        # Update the button to be the length of the text
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def _update_styles(self):
        """Updates the styles for the button."""
        self.style().unpolish(self) # type: ignore
        self.style().polish(self) # type: ignore
        self.update()

    def select(self):
        """Adds the selected class to the button."""
        self.setProperty('selected', True)
        self._update_styles()

    def deselect(self):
        """Removes the selected class from the button."""
        self.setProperty('selected', False)
        self._update_styles()