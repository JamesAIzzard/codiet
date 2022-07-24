from PyQt6 import QtWidgets

import app


class SearchWidgetCtrl(app.CodietCtrl):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Call out widgets for intellisense
        self.view: app.SearchWidgetView