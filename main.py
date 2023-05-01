import sys

from PySide6 import QtCore, QtWidgets

from gui.gui_connect.new_main_connect import MainWindows

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    # QApplication.setStyle(QStyleFactory.create('Fusion'))
    main_window = MainWindows()
    main_window.ui.show()
    sys.exit(app.exec())
