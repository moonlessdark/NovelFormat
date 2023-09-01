import sys

from PySide6 import QtWidgets, QtCore, QtGui


class QLeftTabWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.main_width: int = 300
        self.main_high: int = 400

        """
        主界面
        """

        self.widget_main_page = QtWidgets.QWidget(self)

        self.widget_main_button = QtWidgets.QWidget(self)

        self.button_down_text = QtWidgets.QPushButton(self.widget_main_page)
        self.button_format_text = QtWidgets.QPushButton(self.widget_main_page)
        self.button_reset_page = QtWidgets.QPushButton(self.widget_main_page)
        self.button_down_text.setText("D")
        self.button_format_text.setText("F")
        self.button_reset_page.setText("R")

        self.lay_out_main_page = QtWidgets.QVBoxLayout(self.widget_main_page)
        self.lay_out_main_page.setContentsMargins(0, 0, 0, 0)
        self.lay_out_main_page.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_out_main_page.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.lay_out_main_page.addWidget(self.button_down_text, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_out_main_page.addWidget(self.button_format_text, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_out_main_page.addWidget(self.button_reset_page, QtCore.Qt.AlignmentFlag.AlignCenter)

        self.line_left = QtWidgets.QFrame(self.widget_main_page)
        self.line_left.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_left.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line_right = QtWidgets.QFrame(self)
        self.line_right.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_right.setFrameShadow(QtWidgets.QFrame.Sunken)

        """
        下载界面
        """
        self.widget_down_page = QtWidgets.QWidget(self)

        self.widget_down_page_param = QtWidgets.QWidget(self.widget_down_page)

        self.combox_select_down_type = QtWidgets.QComboBox(self.widget_down_page_param)
        self.combox_select_down_type.addItems(["批量下载", "单章下载"])

        self.line_edit_input_website_url = QtWidgets.QTextEdit(self.widget_down_page_param)
        self.line_edit_input_website_url.setPlaceholderText("请输入下载的url")

        self.combox_select_save_type = QtWidgets.QComboBox(self.widget_down_page_param)
        self.combox_select_save_type.addItems(["单文件", "多文件"])

        self.button_set_save_folder = QtWidgets.QPushButton(self.widget_down_page_param)
        self.button_set_save_folder.setText("保存目录")

        self.button_open_save_folder = QtWidgets.QPushButton(self.widget_down_page_param)
        self.button_open_save_folder.setText("打开目录")

        self.button_execute_down_text = QtWidgets.QPushButton(self.widget_down_page_param)
        self.button_execute_down_text.setText("开始下载")

        self.lay_out = QtWidgets.QGridLayout(self.widget_down_page_param)
        self.lay_out.setSpacing(9)
        self.lay_out.setContentsMargins(10, 10, 20, 10)

        """
        日志打印控件
        """
        self.widget_log_page = QtWidgets.QWidget(self.widget_down_page)
        # self.widget_log_page.setStyleSheet("border: 1px solid black;")
        self.log_print = QtWidgets.QPlainTextEdit(self.widget_log_page)

        self.lay_out.addWidget(self.line_edit_input_website_url, 0, 0, 1, 3)
        self.lay_out.addWidget(self.button_set_save_folder, 2, 0)
        self.lay_out.addWidget(self.button_open_save_folder, 2, 1)
        self.lay_out.addWidget(self.button_execute_down_text, 2, 2)
        self.lay_out.addWidget(self.combox_select_down_type, 3, 0)
        self.lay_out.addWidget(self.combox_select_save_type, 3, 1)

        """
        格式化文本
        """
        self.widget_format_page = QtWidgets.QWidget(self)
        # self.widget_format_page.setStyleSheet("border: 1px solid black;")

        self.line_left_format = QtWidgets.QFrame(self.widget_format_page)
        self.line_left_format.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_left_format.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.widget_opt_file = QtWidgets.QWidget(self.widget_format_page)
        self.manual_file_item_list = QtWidgets.QListWidget(self.widget_opt_file)

        self.widget_opt_file_button = QtWidgets.QWidget(self.widget_format_page)

        self.layout_opt_file_button = QtWidgets.QGridLayout(self.widget_opt_file_button)
        self.layout_opt_file_button.setSpacing(1)

        self.manual_button_get_file_list = QtWidgets.QPushButton(self.widget_opt_file_button)
        self.manual_button_get_file_list.setText("打开文件")

        self.manual_button_save_file = QtWidgets.QPushButton(self.widget_opt_file_button)
        self.manual_button_save_file.setText("保存文件")

        self.manual_button_other_save_file = QtWidgets.QPushButton(self.widget_opt_file_button)
        self.manual_button_other_save_file.setText("另存为")

        self.layout_opt_file_button.addWidget(self.manual_button_get_file_list, 0, 0)
        self.layout_opt_file_button.addWidget(self.manual_button_save_file, 0, 1)
        self.layout_opt_file_button.addWidget(self.manual_button_other_save_file, 1, 0)

        self.widget_opt_text = QtWidgets.QWidget(self.widget_format_page)
        # self.widget_opt_text.setStyleSheet("border: 1px solid black;")

        self.manual_button_execute_mode = QtWidgets.QPushButton(self.widget_opt_text)
        self.manual_button_execute_mode.setText("开始执行")

        self.manual_comboBox_select_format_mode = QtWidgets.QComboBox(self.widget_opt_text)
        self.manual_comboBox_select_format_mode.addItems(["无", "换行校验", "词语纠错", "去除广告"])

        self.manual_input_select_text = QtWidgets.QLineEdit(self.widget_opt_text)
        self.manual_input_select_text.setPlaceholderText("请输入需要查询的内容")
        self.manual_input_replace_text = QtWidgets.QLineEdit(self.widget_opt_text)
        self.manual_input_replace_text.setPlaceholderText("请输入需要替换的内容")
        self.manual_button_select_text = QtWidgets.QPushButton(self.widget_opt_text)
        self.manual_button_select_text.setText("查询")
        self.manual_button_replace_text = QtWidgets.QPushButton(self.widget_opt_text)
        self.manual_button_replace_text.setText("替换")
        self.manual_button_replace_text_all = QtWidgets.QPushButton(self.widget_opt_text)
        self.manual_button_replace_text_all.setText("替换全部")

        self.layout_opt_text_button = QtWidgets.QGridLayout(self.widget_opt_text)
        self.layout_opt_text_button.setContentsMargins(1, 10, 1, 1)
        self.layout_opt_text_button.addWidget(self.manual_comboBox_select_format_mode, 0, 0)
        self.layout_opt_text_button.addWidget(self.manual_button_execute_mode, 0, 1)
        self.layout_opt_text_button.addWidget(self.manual_input_select_text, 1, 0, 1, 2)
        self.layout_opt_text_button.addWidget(self.manual_input_replace_text, 2, 0, 1, 2)
        self.layout_opt_text_button.addWidget(self.manual_button_select_text, 3, 0)
        self.layout_opt_text_button.addWidget(self.manual_button_replace_text, 3, 1)
        self.layout_opt_text_button.addWidget(self.manual_button_replace_text_all, 4, 0)

        self.widget_novel_content = QtWidgets.QWidget(self.widget_format_page)
        self.novel_edit_print = QtWidgets.QTextEdit(self.widget_novel_content)
        self.novel_edit_print.setPlaceholderText("等待加载小说内容")
        self._set_ui_init()

        """
        ui connect
        """
        self.button_down_text.clicked.connect(self.load_down_ui)
        self.button_format_text.clicked.connect(self.load_format_ui)
        self.button_reset_page.clicked.connect(self._set_ui_init)

    def _set_ui_init(self):
        """
        主界面初始化
        :return:
        """

        self.setWindowTitle("NovelEditTools")
        self.setMinimumSize(self.main_width, self.main_high)

        self.button_down_text.setFixedSize(100, 100)
        self.button_format_text.setFixedSize(100, 100)

        self.button_reset_page.hide()  # 隐藏重置按钮
        self.line_left.hide()  # 隐藏左侧菜单分割线
        self.line_left_format.hide()  # 隐藏格式化的右侧分割线
        self.line_right.hide()  # 隐藏右侧功能分割线
        self.widget_down_page.hide()  # 隐藏下载界面
        self.widget_format_page.hide()  # 隐藏格式化界面
        self.widget_log_page.hide()  # 隐藏日志打印控件

        self.widget_main_page.setGeometry(QtCore.QRect(0, 0, self.main_width, self.main_high))
        self.__center()

    def _min_left_widget(self):
        """
        将主窗口缩小到左侧
        :return:
        """
        if self.line_left.isVisible():
            return None
        # 先将按钮靠左显示
        button_fix: int = 40
        self.widget_main_page.setGeometry(QtCore.QRect(0, 0, 50, self.main_high))
        self.button_down_text.setFixedSize(button_fix, button_fix)
        self.button_format_text.setFixedSize(button_fix, button_fix)
        self.button_reset_page.setFixedSize(button_fix, button_fix)

        # 加载一下左侧的分界线
        self.line_left.setGeometry(QtCore.QRect(49, 5, 3, 390))
        self.line_left.show()
        # 加载一下重置界面的按钮
        self.button_reset_page.show()

        self.__center()

    def load_down_ui(self):
        """
        加载下载界面
        :return:
        """
        self._min_left_widget()
        if self.widget_format_page.isVisible():
            """
            如果格式化界面此时是显示状态
            """
            self.widget_format_page.close()
        self.setFixedSize(self.main_width, self.main_high)

        self.setWindowTitle("NovelDownload")

        self.widget_down_page.setGeometry(QtCore.QRect(45, 0, 268, 400))
        self.widget_down_page_param.setGeometry(QtCore.QRect(0, 0, 268, 190))
        self.widget_down_page.show()

        # 加载一个功能分割线
        self.line_right.setGeometry(QtCore.QRect(55, 190, 238, 3))
        self.line_right.show()

        # 加载日志控件的位置
        self.widget_log_page.show()
        self.widget_log_page.setGeometry(QtCore.QRect(10, 200, 238, 200))
        self.log_print.setFixedSize(238, 190)
        self.log_print.setPlaceholderText("日志打印...")
        self.log_print.setOverwriteMode(False)
        self.__center()

    def __center(self):
        # 获取屏幕的尺寸信息
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        # 获取窗口的尺寸信息
        size = self.geometry()
        # 将窗口移动到指定位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def load_format_ui(self):
        """
        加载格式化界面
        :return:
        """
        self._min_left_widget()

        if self.widget_down_page.isVisible():
            """
            如果下载界面此时是显示状态
            """
            self.widget_down_page.close()
        f_width: int = 900
        f_high: int = 600
        self.setFixedSize(f_width, f_high)
        self.setWindowTitle("NovelFormats")

        self.widget_format_page.setGeometry(QtCore.QRect(60, 0, f_width - 65, f_high))
        self.widget_format_page.show()

        self.widget_opt_file.setGeometry(QtCore.QRect(0, 10, 200, 120))
        self.widget_opt_file_button.setGeometry(QtCore.QRect(0, 125, 200, 70))

        # 加载一个功能分割线
        self.line_right.setGeometry(QtCore.QRect(60, 195, 205, 3))
        self.line_right.show()

        # 加载一下按钮区域
        self.widget_opt_text.setGeometry(QtCore.QRect(0, 200, 200, 170))

        # 加载一个右侧分割线
        self.line_left_format.setGeometry(QtCore.QRect(210, 5, 3, 390))
        self.line_left_format.show()

        self.widget_novel_content.setGeometry(QtCore.QRect(220, 10, f_width - 285, f_high - 20))
        self.novel_edit_print.setFixedSize(f_width - 285, f_high - 20)
        self.__center()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QLeftTabWidget()
    main_window.show()
    sys.exit(app.exec())
