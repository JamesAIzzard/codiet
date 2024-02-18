from datetime import datetime

from codiet.views.serve_time_intervals_editor_view import ServeTimeIntervalsEditorView


class ServeTimeIntervalsEditorCtrl:
    def __init__(self, view: ServeTimeIntervalsEditorView):
        self.view = view
        self.time_intervals: list[tuple[datetime, datetime]] = []

        # Connect the signals and slots
        self.view.btn_add_time_window.clicked.connect(self.on_add_time_interval_clicked)
        self.view.btn_remove_time_window.clicked.connect(self.on_remove_time_interval_clicked)

    @property
    def selected_time_window_text(self) -> str:
        """Return the text of the selected time window."""
        current_item = self.view.lst_time_intervals.currentItem()
        if current_item is not None:
            return current_item.text()
        else:
            return ""

    def _parse_time_interval(self, time_str: str) -> tuple[datetime, datetime]:
        """
        Parses a string representing a time interval into a tuple of two timestamps.

        Args:
            time_str: A string containing two times separated by a hyphen.

        Returns:
            A tuple of two datetime objects representing the start and end times of the interval.

        Raises:
            ValueError: If the string cannot be parsed into a valid time interval.
        """

        try:
            # Split the string into two parts
            start_time_str, end_time_str = time_str.split("-")

            # Parse each time string into a datetime object
            start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
            end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()

            # Combine the times with a reference date
            today = datetime.today()
            start_timestamp = datetime.combine(today, start_time)
            end_timestamp = datetime.combine(today, end_time)

            return start_timestamp, end_timestamp

        except ValueError as e:
            raise ValueError(f"Invalid time interval format: {time_str}") from e


    def on_add_time_interval_clicked(self):
        """Handle the user clicking the add button."""
        self.view.show_time_interval_popup()

    def on_remove_time_interval_clicked(self):
        """Handle the user clicking the remove button."""
        index = self.view.selected_index
        if index >= 0:
            self.view.remove_time_interval(index)