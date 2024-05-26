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

class SaveButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='save-icon.png',
            text='Save',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class SaveJSONButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='save-icon.png',
            text='Save JSON',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(150)

class OKButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='ok-icon.png',
            text='OK',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class AddButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='add-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class RemoveButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='remove-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class EditButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='edit-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class DeleteButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='delete-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class ClearButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='cancel-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class ConfirmButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='ok-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class SolveButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='solve-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)

class AutopopulateButton(IconButton):
    def __init__(self, *args, **kwargs):
        super().__init__(
            icon_filename='autopopulate-icon.png',
            *args,
            **kwargs
        )
        # Set the maximum width
        self.setMaximumWidth(50)