from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
)
from PyQt6.QtCore import pyqtSignal

from codiet.views.buttons import AddButton, RemoveButton

class ServeTimeIntervalsEditorView(QWidget):
    """UI element to allow the user to edit the serve time intervals."""

    # Define signals
    addServeTimeClicked = pyqtSignal()
    removeServeTimeClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        """Build the UI for the serve time intervals editor."""
        # Create vertical layout as the top level
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)
        # Reduce the vertical padding in this layout
        lyt_top_level.setContentsMargins(0, 0, 0, 0)

        # Create a groupbox inside this layout
        grp_serve_times = QGroupBox("Serve Time Intervals")
        lyt_top_level.addWidget(grp_serve_times)

        # Create a vertical layout inside the groupbox
        lyt_serve_times = QVBoxLayout()
        grp_serve_times.setLayout(lyt_serve_times)
        # Reduce the vertical padding in this layout
        lyt_serve_times.setContentsMargins(5, 5, 5, 5)

        # Inside the vertical layout, create a horizontal layout for the buttons
        lyt_buttons = QHBoxLayout()
        lyt_serve_times.addLayout(lyt_buttons)

        # Create a button to add a time window
        self.btn_add_time_window = AddButton()
        lyt_buttons.addWidget(self.btn_add_time_window)
        self.btn_add_time_window.clicked.connect(self.addServeTimeClicked)
        # Create a button to remove a time window
        self.btn_remove_time_window = RemoveButton()
        lyt_buttons.addWidget(self.btn_remove_time_window)
        self.btn_remove_time_window.clicked.connect(self.removeServeTimeClicked)
        # Push buttons to LHS
        lyt_buttons.addStretch()

        # Create a list widget to hold the time windows
        self.lst_time_intervals = QListWidget()
        lyt_serve_times.addWidget(self.lst_time_intervals)

    @property
    def time_intervals(self) -> list[str]:
        """Return the list of time intervals."""
        intervals = []
        for i in range(self.lst_time_intervals.count()):
            item = self.lst_time_intervals.item(i)
            intervals.append(item.text())  # type: ignore
        return intervals

    @property
    def selected_index(self) -> int | None:
        """Return the index of the selected time interval."""
        if self.interval_is_selected:
            return self.lst_time_intervals.currentRow()
        else:
            return None

    @property
    def interval_is_selected(self) -> bool:
        """Return whether a time interval is selected."""
        return self.lst_time_intervals.currentItem() is not None

    @property
    def selected_time_interval_string(self) -> str | None:
        """Return the selected time interval."""
        if not self.interval_is_selected:
            return None
        else:
            return self.lst_time_intervals.currentItem().text()  # type: ignore

    def update_serve_times(self, time_intervals: list[str]) -> None:
        """Update the list of time intervals."""
        # First clear the existing list
        self.lst_time_intervals.clear()
        # Add each time interval to the list
        for time_interval in time_intervals:
            self.add_time_interval(time_interval)

    def add_time_interval(self, time_interval: str):
        """Add a time interval to the list."""
        # Check the string is not already in the list
        for i in range(len(self.lst_time_intervals)):
            if self.lst_time_intervals.item(i).text() == time_interval:  # type: ignore
                return
        # Add the time interval to the list
        self.lst_time_intervals.addItem(time_interval)

    def remove_time_interval(self, index: int):
        """Remove a time interval from the list."""
        self.lst_time_intervals.takeItem(index)

    def clear(self):
        """Clear the list of time intervals."""
        self.lst_time_intervals.clear()
