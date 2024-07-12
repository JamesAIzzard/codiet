from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget

from codiet.views.units.unit_dropdown import UnitDropdown

class StandardUnitEditorView(QWidget):
    """A widget for editing the standard unit of an ingredient.
    
    Signals:
        onUnitChanged: Emitted when the standard unit is changed.
            Has a single argument, the new standard unit id (int).
    """

    onUnitChanged = pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        """Initialise the standard unit editor view."""
        super().__init__(*args, **kwargs)
        
        # Build the UI
        self._build_ui()

        # Connect signals and slots
        self.unit_dropdown.currentIndexChanged.connect(self._on_unit_changed)

    def _on_unit_changed(self) -> None:
        """Called when the standard unit is changed."""
        self.onUnitChanged.emit(self.unit_dropdown.selected_unit_id)

    def _build_ui(self):
        """Constructs the user interface."""
        # Create a horizontal layout
        layout = QHBoxLayout()
        self.setLayout(layout)
        # Create a label
        lbl_standard_unit = QLabel("Standard Unit:")
        layout.addWidget(lbl_standard_unit)
        # Create unit editor
        self.unit_dropdown = UnitDropdown()
        layout.addWidget(self.unit_dropdown)
        # Add a spacer to push the combo box to the LHS
        layout.addStretch()
