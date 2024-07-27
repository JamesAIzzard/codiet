import sys, logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from codiet.views.dialogs.icon_message_dialog_view import IconMessageDialogView
from codiet.controllers.dialogs.base_dialog import BaseDialog
from codiet.controllers.dialogs.icon_message_dialog import IconMessageDialog
from codiet.controllers.dialogs.icon_message_buttons_dialog import IconMessageButtonsDialog
from codiet.controllers.dialogs.confirm_dialog import ConfirmDialog
from codiet.controllers.dialogs.error_dialog import ErrorDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Application")
        self.setGeometry(100, 100, 600, 400)

        button = QPushButton("Open Dialog", self)
        button.clicked.connect(self.show_dialog)
        self.setCentralWidget(button)

    def show_dialog(self):
        # dialog = BaseDialog(
        #     parent=self,
        #     title="Test Dialog",
        # )
        # dialog = IconMessageDialog(
        #     parent=self,
        #     title="Test Dialog",
        #     message="This is a test message.",
        # )
        # Create a close button
        # close_button = QPushButton("Close")
        # close_button.clicked.connect(lambda: print("clicked"))
        # dialog = IconMessageButtonsDialog(
        #     parent=self,
        #     title="Buttons Dialog",
        #     message="I'm a buttons dialog.",
        #     buttons=[
        #         QPushButton("Button 1"),
        #         close_button,
        #     ]
        # )
        dialog = ErrorDialog(parent=self, title="Error!", message="An error occurred.")
        dialog.okClicked.connect(lambda: dialog.close())
        dialog.show()

def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Set to DEBUG for development, INFO or WARNING for production
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stderr),
            # You can add file handlers here if you want to log to a file as well
        ]
    )

if __name__ == "__main__":
    configure_logging()
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())