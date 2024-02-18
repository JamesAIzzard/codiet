from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

if TYPE_CHECKING:
    from codiet.views.serve_time_intervals_editor_view import ServeTimeIntervalsEditorView

class TimeIntervalPopupView(QDialog):
    def __init__(self, parent:'ServeTimeIntervalsEditorView'):
        super().__init__()

        # Stash the parent view instance
        self.serve_time_intervals_editor_view = parent

        self.setWindowTitle("Time Interval")
        # self.resize(400, 300)

        # Create a layout for the dialog
        lyt_top_level = QVBoxLayout()
        self.setLayout(lyt_top_level)

        # Create a horizontal layout for the time intervals and hyphen
        lyt_time_interval = QHBoxLayout()
        lyt_top_level.addLayout(lyt_time_interval)

        # Add the Start time interval
        self.txt_start_time = QLineEdit()
        lyt_time_interval.addWidget(self.txt_start_time)
        
        # Add the hyphen
        lbl_hyphen = QLabel(" - ")
        lyt_time_interval.addWidget(lbl_hyphen)

        # Add the End time interval
        self.txt_end_time = QLineEdit()
        lyt_time_interval.addWidget(self.txt_end_time)

        # Add the add button
        self.btn_add = QPushButton("Add")
        lyt_top_level.addWidget(self.btn_add)

        # Connect the add button to the on_add_clicked method
        self.btn_add.clicked.connect(self.on_add_clicked)

    @property
    def time_interval_string(self) -> str:
        """Return the string representing the time interval."""
        return f"{self.txt_start_time.text()} - {self.txt_end_time.text()}"

    def on_add_clicked(self):
        """Handle the user clicking the add button."""
        self.serve_time_intervals_editor_view.add_time_interval(self.time_interval_string)

    def show(self):
        self.exec()
