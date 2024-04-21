from typing import Callable
from datetime import datetime

from codiet.views.serve_time_intervals_editor_view import ServeTimeIntervalsEditorView
from codiet.views.time_interval_popup_view import TimeIntervalPopupView
from codiet.views.dialog_box_view import ErrorDialogBoxView
from codiet.controllers.time_interval_popup_ctrl import TimeIntervalPopupCtrl


class ServeTimeIntervalsEditorCtrl:
    def __init__(
        self,
        view: ServeTimeIntervalsEditorView,
        on_add_time_interval: Callable[[tuple[datetime, datetime]], None],
        on_remove_time_interval: Callable[[tuple[datetime, datetime]], None],
    ):
        self.view = view
        self.on_add_time_interval = on_add_time_interval
        self.on_remove_time_interval = on_remove_time_interval
        self.error_dialog: ErrorDialogBoxView | None = None

        # Connect the signals and slots
        self.view.btn_add_time_window.clicked.connect(self.on_add_time_interval_clicked)
        self.view.btn_remove_time_window.clicked.connect(
            self.on_remove_time_interval_clicked
        )

    def on_add_time_interval_clicked(self) -> None:
        """Handle the user clicking the add button."""
        try:
            # Try and collect the time interval from the user
            time_interval = self.show_time_interval_popup()            
        # If the user puts in an invalid time
        except ValueError as e:
            # Show them an error dialog
            self.show_invalid_time_interval_popup()
            return
        # If we got None, just return
        if time_interval is None:
            return None
        # We got an interval
        # If the interval is already in the list
        if self.interval_in_list(time_interval):
            # Just return None and don't do anything else
            return None
        # Interval isn't in list, so add it to the list
        self.view.add_time_interval(self.convert_datetime_interval_to_time_string(time_interval))
        # Call the on_add_time_interval function with the interval
        self.on_add_time_interval((time_interval[0], time_interval[1]))

    def interval_in_list(self, time_interval: tuple[datetime, datetime]) -> bool:
        """Check if a time interval is already in the list."""
        # Get the time string
        time_str = self.convert_datetime_interval_to_time_string(time_interval)
        # Check if the string is in the list
        return time_str in self.view.time_intervals

    def show_time_interval_popup(self) -> tuple[datetime, datetime] | None:
        """Show the time interval popup and return the entered time interval."""
        # Init the popup view and controller
        time_interval_popup_ctrl = TimeIntervalPopupCtrl(TimeIntervalPopupView())
        # Show the popup
        time_interval_popup_ctrl.view.show()
        # Return the contents of the popup
        return time_interval_popup_ctrl.time_interval

    def show_invalid_time_interval_popup(self):
        """Show a popup indicating an invalid time interval was entered."""
        # Ensure that only one instance of the dialog is created, or reuse the existing one
        if self.error_dialog is None:
            self.error_dialog = ErrorDialogBoxView(
                message="Invalid time interval format. Please enter the time interval in the format HH:MM:SS - HH:MM:SS.",
                title="Invalid Time Interval"
            )
        self.error_dialog.exec()  # Using exec() to make the dialog modal

    def on_remove_time_interval_clicked(self):
        """Handle the user clicking the remove button."""
        index = self.view.selected_index
        if index >= 0:
            self.view.remove_time_interval(index)

    def convert_time_string_to_datetime_interval(self, time_str: str) -> tuple[datetime, datetime]:
        """Convert a time string to a datetime interval."""
        # Split the string into two parts
        start_str, end_str = time_str.split(" - ")
        # Convert the strings to datetime objects
        start_time = datetime.strptime(start_str, "%H:%M")
        end_time = datetime.strptime(end_str, "%H:%M")
        return start_time, end_time
    
    def convert_datetime_interval_to_time_string(self, time_interval: tuple[datetime, datetime]) -> str:
        """Convert a datetime interval to a time string."""
        # Convert the datetime objects to strings
        start_str = time_interval[0].strftime("%H:%M")
        end_str = time_interval[1].strftime("%H:%M")
        return f"{start_str} - {end_str}"

    def _connect_signals_and_slots(self) -> None:
        """Connect the signals and slots."""
        self.view.btn_add_time_window.clicked.connect(self.on_add_time_interval_clicked)
        self.view.btn_remove_time_window.clicked.connect(
            self.on_remove_time_interval_clicked
        )
