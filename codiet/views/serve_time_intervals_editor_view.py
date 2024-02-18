from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
)

from codiet.views.time_interval_popup_view import TimeIntervalPopupView

class ServeTimeIntervalsEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Instantiate the popup for adding a time interval
        self.time_interval_popup = TimeIntervalPopupView(parent=self)

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
        self.btn_add_time_window = QPushButton("Add")
        lyt_buttons.addWidget(self.btn_add_time_window)
        # Create a button to remove a time window
        self.btn_remove_time_window = QPushButton("Remove")
        lyt_buttons.addWidget(self.btn_remove_time_window)

        # Create a list widget to hold the time windows
        self.lst_time_intervals = QListWidget()
        lyt_serve_times.addWidget(self.lst_time_intervals)

    @property
    def time_intervals(self) -> list[str]:
        """Return the list of time intervals."""
        intervals = []
        if len(self.lst_time_intervals) > 0:
            for i in range(len(self.lst_time_intervals)):
                intervals.append(self.lst_time_intervals.item(i).text()) # type: ignore
        return []

    @property
    def selected_index(self) -> int:
        """Return the index of the selected time interval."""
        return self.lst_time_intervals.currentRow()

    def add_time_interval(self, time_interval: str):
        """Add a time interval to the list."""
        # First check the string is not already in the list
        for i in range(len(self.lst_time_intervals)):
            if self.lst_time_intervals.item(i).text() == time_interval: # type: ignore
                return
        # Add the time interval to the list
        self.lst_time_intervals.addItem(time_interval)

    def remove_time_interval(self, index: int):
        """Remove a time interval from the list."""
        self.lst_time_intervals.takeItem(index)

    def show_time_interval_popup(self):
        """Show the popup for adding a time interval."""
        self.time_interval_popup.show()