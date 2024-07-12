from PyQt6.QtCore import pyqtSignal, QVariant
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout

from codiet.views.buttons import AddButton, RemoveButton, IconButton
from codiet.views.listbox import ListBox

class UnitConversionsEditorView(QWidget):
    """A widget for defining custom measurement units.
    It is essentially a listbox showing the current unit conversions, with buttons to add, remove, and flip conversions.
    
    Signals:
        addUnitClicked: Emitted when the add unit button is clicked.
            No arguments.
        removeUnitClicked: Emitted when the remove unit button is clicked.
            Has a single argument, the ID of the selected unit (int or None if nothing is selected).
        flipConversionClicked: Emitted when the flip conversion button is clicked.
            Has a single argument, the ID of the selected unit (int or None if nothing is selected).
    """

    addUnitClicked = pyqtSignal()
    removeUnitClicked = pyqtSignal(QVariant)
    flipConversionClicked = pyqtSignal(QVariant)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Build the UI
        self._build_ui()

        # Connect signals
        self.btn_add.clicked.connect(self.addUnitClicked.emit)
        self.btn_remove.clicked.connect(self._on_remove_conversion_clicked)
        self.btn_swap_conversion.clicked.connect(self._on_swap_conversion_clicked)

    @property
    def selected_conversion_id(self) -> int|None:
        """Return the global ID of the selected conversion."""
        if self.conversion_list.item_is_selected:
            return self.conversion_list.selected_item_data
        else:
            return None
        
    @property
    def selected_conversion_view(self) -> QWidget|None:
        """Return the widget of the selected conversion."""
        if self.conversion_list.item_is_selected:
            return self.conversion_list.selected_item_content # type: ignore
        else:
            return None

    def _on_remove_conversion_clicked(self):
        """Called when the remove unit button is clicked."""
        # Emit the signal with the id of the selected measurement, which will be None
        # if nothing is selected. The item data stores the ID.
        self.removeUnitClicked.emit(self.selected_conversion_id)

    def _on_swap_conversion_clicked(self):
        """Called when the swap conversion button is clicked."""
        # Emit the signal with the id of the selected measurement, which will be None
        # if nothing is selected. The item data stores the ID.
        self.removeUnitClicked.emit(self.selected_conversion_id)

    def _build_ui(self):
        """Constructs the user interface."""
        # Create a vertical layout for the widget
        lyt_outer = QVBoxLayout()
        self.setLayout(lyt_outer)
        lyt_outer.setContentsMargins(0, 0, 0, 0)
        # Put a groupbox inside
        grp_measurements = QGroupBox("Unit Conversions")
        lyt_outer.addWidget(grp_measurements)
        # Create a vertical layout for the groupbox
        lyt_top_level = QVBoxLayout()
        grp_measurements.setLayout(lyt_top_level)
        # Create a horizontal layout for the buttons
        lyt_buttons = QHBoxLayout()
        lyt_top_level.addLayout(lyt_buttons)
        # Add the buttons
        self.btn_add = AddButton()
        lyt_buttons.addWidget(self.btn_add)
        self.btn_remove = RemoveButton()
        lyt_buttons.addWidget(self.btn_remove)
        self.btn_swap_conversion = IconButton(
            icon_filename="swap-icon.png",
            text="Swap Conversion",
            tooltip="Flip the conversion"
        )
        # Drop in a spacer to push buttons to lhs
        lyt_buttons.addStretch()
        # Add a listbox of custom measurements
        self.conversion_list = ListBox()
        lyt_top_level.addWidget(self.conversion_list)
