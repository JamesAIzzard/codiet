from datetime import datetime

from codiet.views.time_interval_popup_view import TimeIntervalPopupView

class TimeIntervalPopupCtrl():
    def __init__(self, view: TimeIntervalPopupView):
        self.view = view
        self._connect_signals_and_slots()

    @property
    def time_interval(self) -> tuple[datetime, datetime] | None:
        """Return the time interval."""
        # If either the start or end time are empty, return None
        if self.view.start_time.strip() == '' or self.view.end_time.strip() == '':
            return None
        # Convert the start and end time to datetime objects
        start_time = datetime.strptime(self.view.start_time, "%H:%M")
        end_time = datetime.strptime(self.view.end_time, "%H:%M")
        return start_time, end_time

    def on_add_clicked(self):
        # Close the view
        self.view.accept()

    def _connect_signals_and_slots(self) -> None:
        self.view.btn_add.clicked.connect(self.on_add_clicked)

