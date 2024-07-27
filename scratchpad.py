import sys, logging
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton

from codiet.controllers.dialogs.base_dialog import BaseDialog
from codiet.controllers.dialogs.icon_message_dialog import IconMessageDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Application")
        self.setGeometry(100, 100, 600, 400)

        button = QPushButton("Open Dialog", self)
        button.clicked.connect(self.show_dialog)
        self.setCentralWidget(button)

    def show_dialog(self):
        dialog = IconMessageDialog(
            parent=self,
        )
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