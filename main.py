import sys

from PySide6 import QtWidgets

from NovelGui.QConnect.PageConnect import PageConnect

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = PageConnect()
    main_window.show()
    sys.exit(app.exec())
