from PyQt6 import QtWidgets, QtGui, uic

class MainWindowView(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Bring the ui file in
        uic.load_ui.loadUi("app/mainwindow.ui", self)

        # Define the main widgets
        self.wg_page_stack: QtWidgets.QStackedWidget
        self.btn_ingredients: QtWidgets.QMenu
        self.btn_user_requirements: QtGui.QAction
        self.statusbar: QtWidgets.QStatusBar

        # Write a welcom message to the status bar
        self.statusbar.showMessage("CoDiet V0.1")


    def add_page(self, page_view:QtWidgets.QWidget) -> None:
        """Adds a page widget into the stack."""
        self.wg_page_stack.insertWidget(
            0, page_view
        )

    def change_window(self, page_name: str) -> None:
        """Updates the main window to show the pane with the
        specified ID."""
        # Find the child widget by the name requested
        page = self.wg_page_stack.findChild(QtWidgets.QWidget, page_name)
        # Set the widget as current
        self.wg_page_stack.setCurrentWidget(page) # type:ignore
