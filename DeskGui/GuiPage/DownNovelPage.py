from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Signal

from DeskGui.GuiPage.MainElement import QMainElement


class QSettingHeaderParam(QtWidgets.QWidget):

    param_signal = Signal(str)

    def __init__(self):
        super().__init__()

        self.resize(200, 200)

        self.line_edit_header = QtWidgets.QTextEdit()
        self.line_edit_header.setPlaceholderText("请将从浏览器复制的Curl链接粘贴至此处。")
        self.button_submit_header_param = QtWidgets.QPushButton()
        self.button_submit_header_param.setText("确认")
        self.button_submit_header_param_reset = QtWidgets.QPushButton()
        self.button_submit_header_param_reset.setText("重置")
        self.__load_ui_header_param()

        # connect
        self.button_submit_header_param.clicked.connect(self.submit_param)
        self.button_submit_header_param_reset.clicked.connect(self.reset_param)

    def __load_ui_header_param(self):
        layout_header_param = QtWidgets.QGridLayout(self)
        layout_header_param.addWidget(self.line_edit_header, 0, 0, 2, 2)
        layout_header_param.addWidget(self.button_submit_header_param_reset, 2, 0)
        layout_header_param.addWidget(self.button_submit_header_param, 2, 1)
        layout_header_param.setContentsMargins(5, 5, 5, 5)
        layout_header_param.setSpacing(1)

    def close_widows_header_param(self):
        """
        关闭此窗口
        :return:
        """
        self.close()

    def open_widows_header_param(self):
        """
        显示此窗口
        :return:
        """
        self.line_edit_header.setPlaceholderText("请将从浏览器复制的Curl链接粘贴至此处。")
        self.show()

    def submit_param(self):
        """
        提交参数
        :return:
        """
        param_text: str = self.line_edit_header.toPlainText()
        if param_text == "":
            self.line_edit_header.setPlaceholderText("未在此窗口检测到curl链接")
        else:
            if param_text.find("curl") != 0:
                self.line_edit_header.clear()
                self.line_edit_header.setPlaceholderText("curl链接的格式错误，请检查")
            else:
                self.param_signal.emit(param_text)

    def reset_param(self):
        self.param_signal.emit("")


class QDownNovel(QMainElement):

    def __init__(self):
        super().__init__()

        self.line_edit_input_website_url = QtWidgets.QTextEdit()
        self.line_edit_input_website_url.setPlaceholderText("请输入下载的url")

        self.combox_select_down_mode = QtWidgets.QComboBox()
        self.combox_select_down_mode.addItems(["下载模式一", "下载模式二"])
        self.combox_select_down_mode.setEnabled(False)

        self.combox_select_save_type = QtWidgets.QComboBox()
        self.combox_select_save_type.addItems(["生成单文件", "生成多文件"])

        self.button_set_save_folder = QtWidgets.QPushButton()
        self.button_set_save_folder.setText("保存目录")

        self.button_open_save_folder = QtWidgets.QPushButton()
        self.button_open_save_folder.setText("打开目录")

        self.button_execute_down_text = QtWidgets.QPushButton()
        self.button_execute_down_text.setText("开始下载")

        self.button_setting_req_header_param = QtWidgets.QPushButton()
        self.button_setting_req_header_param.setText("设置请求头")

        self.log_print = QtWidgets.QPlainTextEdit()
        self.log_print.setPlaceholderText("日志打印...")

        self.QRadioButton_down_novel = QtWidgets.QRadioButton()
        self.QRadioButton_down_novel.setText("下载小说")

        self.QRadioButton_down_comic = QtWidgets.QRadioButton()
        self.QRadioButton_down_comic.setText("下载漫画")

        self.__load_ui_down_novel_element()

        # connect
        self.QRadioButton_down_comic.clicked.connect(self.__load_combox_select_down_type_value)
        self.QRadioButton_down_novel.clicked.connect(self.__load_combox_select_down_type_value)

    def __load_combox_select_down_type_value(self):
        """
        加载下载漫画的模式下拉框
        :return:
        """
        if self.QRadioButton_down_comic.isChecked():
            self.combox_select_down_mode.setEnabled(True)
        else:
            self.combox_select_down_mode.setEnabled(False)

    def __load_ui_down_novel_element(self):
        """
        下载小说界面UI
        :return:
        """
        lay_out_down_type = QtWidgets.QHBoxLayout()
        lay_out_down_type.addWidget(self.QRadioButton_down_novel)
        lay_out_down_type.addWidget(self.QRadioButton_down_comic)
        lay_out_down_type.setSpacing(5)

        lay_out_down_novel_param = QtWidgets.QGridLayout()
        lay_out_down_novel_param.addLayout(lay_out_down_type, 0, 0, 1, 3, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        lay_out_down_novel_param.addWidget(self.line_edit_input_website_url, 1, 0, 2, 3)
        lay_out_down_novel_param.addWidget(self.button_set_save_folder, 3, 0)
        lay_out_down_novel_param.addWidget(self.button_open_save_folder, 3, 1)
        lay_out_down_novel_param.addWidget(self.button_execute_down_text, 3, 2)
        lay_out_down_novel_param.addWidget(self.button_setting_req_header_param, 4, 0)
        lay_out_down_novel_param.addWidget(self.combox_select_save_type, 4, 1)
        lay_out_down_novel_param.addWidget(self.combox_select_down_mode, 4, 2)
        lay_out_down_novel_param.setContentsMargins(0, 10, 0, 0)
        lay_out_down_novel_param.setSpacing(10)

        lay_out_down_novel = QtWidgets.QVBoxLayout()
        lay_out_down_novel.addLayout(lay_out_down_novel_param, 1)
        lay_out_down_novel.addWidget(self.log_print, 1)
        lay_out_down_novel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        lay_out_down_novel.setContentsMargins(0, 0, 0, 0)
        lay_out_down_novel.setSpacing(5)

        # 下载界面加载布局
        self.stack_widget_down_content.setLayout(lay_out_down_novel)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = QSettingHeaderParam()
    main_window.show()
    sys.exit(app.exec())
