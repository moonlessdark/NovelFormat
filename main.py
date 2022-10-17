import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QStyleFactory
from gui.gui_connect.new_main_connect import MainWindows


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    main_window = MainWindows()
    main_window.ui.show()
    sys.exit(app.exec())
