from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
)

class ServeTimeIntervalsEditorView(QWidget):
    def __init__(self):
        super().__init__()

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
        self.list_time_windows = QListWidget()
        lyt_serve_times.addWidget(self.list_time_windows)
        # Add some dummy time windows for now
        self.list_time_windows.addItem("Time Window 1")
        self.list_time_windows.addItem("Time Window 2")
        self.list_time_windows.addItem("Time Window 3")        