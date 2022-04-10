from PyQt6 import QtWidgets

from model import User
from gui import MainWindow

# Init the user instance
user = User()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Create an instance of your window and show it
    lw = MainWindow()
    lw.show()

    app.exec()