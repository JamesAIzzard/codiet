from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

class TimeIntervalPopupView(QDialog):
    def __init__(self):
        super().__init__()
        self._build_ui()


    def _build_ui(self):
        """Build the user interface."""
        self.setWindowTitle("Enter Time Interval")

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
    
    @property
    def start_time(self) -> str:
        """Return the start time."""
        return self.txt_start_time.text()
    
    @property
    def end_time(self) -> str:
        """Return the end time."""
        return self.txt_end_time.text()

    def show(self):
        """Show the dialog."""
        self.exec()
