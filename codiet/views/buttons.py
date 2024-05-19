from PyQt6.QtWidgets import QPushButton

from codiet.views import load_icon

class IconButton(QPushButton):
    def __init__(self, icon_filename:str, text:str|None=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the icon
        self.setIcon(load_icon(icon_filename))
        # If the text is set, set it
        if text is not None:
            self.setText(text)


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