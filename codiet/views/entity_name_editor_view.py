from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel

from codiet.views.icon_button import IconButton
from codiet.views.text_editors.line_editor import LineEditor

class EntityNameEditorView(QWidget):
    """The UI view element that displays an entity name as readonly, with an edit button."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._build_ui()

    def _build_ui(self):
        """Instantiates the user interface."""
        # Create the top level layout
        lyt_top_level = QHBoxLayout()
        self.setLayout(lyt_top_level)

        # Create a label and add it to the layout
        label = QLabel("Name:")
        lyt_top_level.addWidget(label)

        # Create a textbox and add it to the layout
        self.txt_ingredient_name = LineEditor()
        # Make the line edit not editable
        self.txt_ingredient_name.setReadOnly(True)
        lyt_top_level.addWidget(self.txt_ingredient_name)

        # Add an edit button
        self.btn_edit = IconButton(icon_filename="edit-icon.png")
        lyt_top_level.addWidget(self.btn_edit)
        # Reduce the vertical padding in this layout
        lyt_top_level.setContentsMargins(0, 0, 0, 0)        