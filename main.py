from PyQt6 import QtWidgets

import model, gui

if __name__ == "__main__":
    # Init the user instance
    user = model.User()

    # Instantiate the gui
    app = QtWidgets.QApplication([])
    main_window_view = gui.MainWindowView()
    main_window_ctrl = gui.MainWindowCtrl(main_window_view)
    
    # Show the gui
    main_window_view.show()
    app.exec()