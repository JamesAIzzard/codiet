from PyQt6 import QtWidgets, uic, QtGui

class MainWindowView(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bring the ui file in
        uic.load_ui.loadUi("gui/mainwindow.ui", self)

    def add_page(self, page_view:QtWidgets.QWidget) -> None:
        """Adds a page widget into the stack."""
        self.wg_page_stack.insertWidget(  # type: ignore
            0, page_view
        )

    def change_window(self, page_name: str) -> None:
        """Updates the main window to show the pane with the
        specified ID."""
        # Find the child widget by the name requested
        page = self.wg_page_stack.findChild(QtWidgets.QWidget, page_name)  # type: ignore
        # Set the widget as current
        self.wg_page_stack.setCurrentWidget(page) # type: ignore
