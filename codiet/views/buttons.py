from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon

class SaveButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set the text
        self.setText("Save")
        
        # Set the icon
        self.setIcon(QIcon('codiet/resources/icons/save-icon.png'))
        
        # Set the maximum width
        self.setMaximumWidth(50)

class AddButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the icon
        self.setIcon(QIcon('codiet/resources/icons/add-icon.png'))
        
        # Set the maximum width
        self.setMaximumWidth(50)

class RemoveButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the icon
        self.setIcon(QIcon('codiet/resources/icons/remove-icon.png'))
        
        # Set the maximum width
        self.setMaximumWidth(50)

class ClearButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the icon
        self.setIcon(QIcon('codiet/resources/icons/cancel-icon.png'))
        
        # Set the maximum width
        self.setMaximumWidth(50)

class ConfirmButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the icon
        self.setIcon(QIcon('codiet/resources/icons/ok-icon.png'))
        
        # Set the maximum width
        self.setMaximumWidth(50)

class SolveButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the icon
        self.setIcon(QIcon('codiet/resources/icons/solve-icon.png'))
        
        # Set the maximum width
        self.setMaximumWidth(50)