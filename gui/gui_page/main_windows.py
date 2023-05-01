# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_windowsfrdwXn.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QPlainTextEdit, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 600)
        MainWindow.setMinimumSize(QSize(700, 600))
        MainWindow.setMaximumSize(QSize(700, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 10, 680, 141))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.input_save_novel_path_by_page = QLineEdit(self.tab)
        self.input_save_novel_path_by_page.setObjectName(u"input_save_novel_path_by_page")
        self.input_save_novel_path_by_page.setGeometry(QRect(260, 70, 171, 22))
        self.down_button_save_path = QPushButton(self.tab)
        self.down_button_save_path.setObjectName(u"down_button_save_path")
        self.down_button_save_path.setGeometry(QRect(181, 65, 71, 32))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(13)
        self.down_button_save_path.setFont(font)
        self.button_download_start_executr = QPushButton(self.tab)
        self.button_download_start_executr.setObjectName(u"button_download_start_executr")
        self.button_download_start_executr.setGeometry(QRect(480, 40, 71, 32))
        self.select_download_type = QComboBox(self.tab)
        self.select_download_type.addItem("")
        self.select_download_type.addItem("")
        self.select_download_type.addItem("")
        self.select_download_type.setObjectName(u"select_download_type")
        self.select_download_type.setGeometry(QRect(221, 10, 135, 25))
        self.select_download_type.setFont(font)
        self.label_down_website = QLabel(self.tab)
        self.label_down_website.setObjectName(u"label_down_website")
        self.label_down_website.setGeometry(QRect(161, 12, 52, 19))
        self.label_down_website.setFont(font)
        self.select_download_mode = QComboBox(self.tab)
        self.select_download_mode.addItem("")
        self.select_download_mode.addItem("")
        self.select_download_mode.setObjectName(u"select_download_mode")
        self.select_download_mode.setGeometry(QRect(360, 10, 102, 25))
        self.select_download_mode.setFont(font)
        self.label_down_file_path = QLabel(self.tab)
        self.label_down_file_path.setObjectName(u"label_down_file_path")
        self.label_down_file_path.setGeometry(QRect(190, 41, 52, 19))
        self.label_down_file_path.setFont(font)
        self.input_download_url = QLineEdit(self.tab)
        self.input_download_url.setObjectName(u"input_download_url")
        self.input_download_url.setGeometry(QRect(260, 41, 171, 22))
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.manual_file_item_list = QListWidget(self.tab_3)
        self.manual_file_item_list.setObjectName(u"manual_file_item_list")
        self.manual_file_item_list.setGeometry(QRect(15, 0, 211, 100))
        self.manual_file_item_list.setFont(font)
        self.label_5 = QLabel(self.tab_3)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(360, 6, 53, 21))
        self.manual_button_execute_mode = QPushButton(self.tab_3)
        self.manual_button_execute_mode.setObjectName(u"manual_button_execute_mode")
        self.manual_button_execute_mode.setGeometry(QRect(590, 0, 57, 32))
        self.manual_comboBox_select_format_mode = QComboBox(self.tab_3)
        self.manual_comboBox_select_format_mode.addItem("")
        self.manual_comboBox_select_format_mode.addItem("")
        self.manual_comboBox_select_format_mode.addItem("")
        self.manual_comboBox_select_format_mode.addItem("")
        self.manual_comboBox_select_format_mode.addItem("")
        self.manual_comboBox_select_format_mode.setObjectName(u"manual_comboBox_select_format_mode")
        self.manual_comboBox_select_format_mode.setGeometry(QRect(420, 3, 130, 28))
        self.line_2 = QFrame(self.tab_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(330, 0, 15, 100))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.line_3 = QFrame(self.tab_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(337, 30, 321, 20))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.manual_input_select_text = QLineEdit(self.tab_3)
        self.manual_input_select_text.setObjectName(u"manual_input_select_text")
        self.manual_input_select_text.setGeometry(QRect(350, 46, 150, 22))
        self.manual_input_replace_text = QLineEdit(self.tab_3)
        self.manual_input_replace_text.setObjectName(u"manual_input_replace_text")
        self.manual_input_replace_text.setGeometry(QRect(510, 46, 150, 22))
        self.manual_button_select_text = QPushButton(self.tab_3)
        self.manual_button_select_text.setObjectName(u"manual_button_select_text")
        self.manual_button_select_text.setGeometry(QRect(360, 73, 57, 32))
        self.manual_button_replace_text = QPushButton(self.tab_3)
        self.manual_button_replace_text.setObjectName(u"manual_button_replace_text")
        self.manual_button_replace_text.setGeometry(QRect(500, 73, 57, 32))
        self.manual_button_replace_text_all = QPushButton(self.tab_3)
        self.manual_button_replace_text_all.setObjectName(u"manual_button_replace_text_all")
        self.manual_button_replace_text_all.setGeometry(QRect(570, 73, 83, 32))
        self.layoutWidget = QWidget(self.tab_3)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(240, 0, 88, 106))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.manual_button_get_file_list = QPushButton(self.layoutWidget)
        self.manual_button_get_file_list.setObjectName(u"manual_button_get_file_list")

        self.verticalLayout.addWidget(self.manual_button_get_file_list)

        self.manual_button_save_file = QPushButton(self.layoutWidget)
        self.manual_button_save_file.setObjectName(u"manual_button_save_file")

        self.verticalLayout.addWidget(self.manual_button_save_file)

        self.manual_button_other_save_file = QPushButton(self.layoutWidget)
        self.manual_button_other_save_file.setObjectName(u"manual_button_other_save_file")

        self.verticalLayout.addWidget(self.manual_button_other_save_file)

        self.tabWidget.addTab(self.tab_3, "")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 160, 60, 16))
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(70, 160, 620, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.plainTextEdit = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setGeometry(QRect(10, 182, 680, 391))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"NovelEditTools", None))
        self.down_button_save_path.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u76ee\u5f55", None))
        self.button_download_start_executr.setText(QCoreApplication.translate("MainWindow", u"\u5f00\u59cb\u4e0b\u8f7d", None))
        self.select_download_type.setItemText(0, QCoreApplication.translate("MainWindow", u"shubao12.com", None))
        self.select_download_type.setItemText(1, QCoreApplication.translate("MainWindow", u"tmallyh.top", None))
        self.select_download_type.setItemText(2, QCoreApplication.translate("MainWindow", u"aastory.space", None))

        self.label_down_website.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u7f51\u7ad9", None))
        self.select_download_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"\u6279\u91cf\u4e0b\u8f7d", None))
        self.select_download_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5355\u7ae0\u4e0b\u8f7d", None))

        self.label_down_file_path.setText(QCoreApplication.translate("MainWindow", u"\u4e0b\u8f7d\u5730\u5740", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\u7f51\u9875\u4e0b\u8f7d", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u5904\u7406\u6a21\u5f0f", None))
        self.manual_button_execute_mode.setText(QCoreApplication.translate("MainWindow", u"\u6267\u884c", None))
        self.manual_comboBox_select_format_mode.setItemText(0, QCoreApplication.translate("MainWindow", u"\u65e0", None))
        self.manual_comboBox_select_format_mode.setItemText(1, QCoreApplication.translate("MainWindow", u"\u6362\u884c\u6821\u9a8c", None))
        self.manual_comboBox_select_format_mode.setItemText(2, QCoreApplication.translate("MainWindow", u"\u6362\u884c\u6821\u9a8c(\u589e\u5f3a)", None))
        self.manual_comboBox_select_format_mode.setItemText(3, QCoreApplication.translate("MainWindow", u"\u8bcd\u8bed\u7ea0\u9519", None))
        self.manual_comboBox_select_format_mode.setItemText(4, QCoreApplication.translate("MainWindow", u"\u53bb\u9664\u5e7f\u544a", None))

        self.manual_button_select_text.setText(QCoreApplication.translate("MainWindow", u"\u67e5\u8be2", None))
        self.manual_button_replace_text.setText(QCoreApplication.translate("MainWindow", u"\u66ff\u6362", None))
        self.manual_button_replace_text_all.setText(QCoreApplication.translate("MainWindow", u"\u66ff\u6362\u5168\u90e8", None))
        self.manual_button_get_file_list.setText(QCoreApplication.translate("MainWindow", u"\u6253\u5f00\u6587\u4ef6", None))
        self.manual_button_save_file.setText(QCoreApplication.translate("MainWindow", u"\u4fdd\u5b58\u6587\u4ef6", None))
        self.manual_button_other_save_file.setText(QCoreApplication.translate("MainWindow", u"\u53e6\u5b58\u4e3a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\u6587\u672c\u5904\u7406", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u4fe1\u606f\u6253\u5370", None))
    # retranslateUi

