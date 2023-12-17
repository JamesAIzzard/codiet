from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QPushButton,
    QListWidget,
)

class ServeTimesEditorView(QWidget):
    def __init__(self):
        super().__init__()

        # Create vertical layout as the top level
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Reduce the vertical padding in this layout
        layout.setContentsMargins(0, 0, 0, 0)

        # Create a groupbox inside this layout
        serve_times_group = QGroupBox("Serve Times")
        layout.addWidget(serve_times_group)
        serve_times_layout = QVBoxLayout()
        serve_times_group.setLayout(serve_times_layout)

        # Create a button to add a time window
        self.btn_add_time_window = QPushButton("Add Time Window")
        serve_times_layout.addWidget(self.btn_add_time_window)

        # Create a list widget to hold the time windows
        self.list_time_windows = QListWidget()
        serve_times_layout.addWidget(self.list_time_windows)
        # Add some dummy time windows for now
        self.list_time_windows.addItem("Time Window 1")
        self.list_time_windows.addItem("Time Window 2")
        self.list_time_windows.addItem("Time Window 3")        