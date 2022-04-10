from PyQt6 import QtWidgets
from gui import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    # Create an instance of your window and show it
    lw = MainWindow()
    lw.show()

    app.exec()