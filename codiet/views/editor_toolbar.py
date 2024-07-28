from PyQt6.QtWidgets import QToolBar

from codiet.views.icon_button import IconButton

class EditorToolbar(QToolBar):
    """Standard editor toolbar, containing add, remove, autopopulate and save to JSON buttons."""

    def __init__(self, entity_name:str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.btn_add = IconButton(icon_filename="add-icon.png")
        self.btn_add.setToolTip(f"Add new.{entity_name}")
        self.addWidget(self.btn_add)

        self.btn_delete = IconButton(icon_filename="delete-icon.png")
        self.btn_delete.setToolTip(f"Delete selected {entity_name}.")
        self.addWidget(self.btn_delete)

        self.btn_autopopulate = IconButton(icon_filename="autopopulate-icon.png")
        self.btn_autopopulate.setToolTip(f"Autopopulate {entity_name}.")
        self.addWidget(self.btn_autopopulate)
        
        self.btn_json_save = IconButton(icon_filename="save-icon.png", text="Save to JSON")
        self.btn_json_save.setToolTip(f"Save {entity_name} to JSON.")
        self.addWidget(self.btn_json_save)