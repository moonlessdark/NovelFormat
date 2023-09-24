import sys

from PySide6 import QtWidgets, QtCore, QtGui


class QLeftTabWidget(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.is_menu_left: bool = False
        self.lay_out_down_novel = None
        self.lay_out_down_novel_param = None
        self.lay_out_main_page = None

        # self.setStyleSheet("border: 1px solid black;")

        """
        主功能按钮
        """
        self.button_down_text = QtWidgets.QPushButton()
        self.button_format_text = QtWidgets.QPushButton()
        self.button_reset_page = QtWidgets.QPushButton()

        self.line_left = QtWidgets.QFrame()
        self.line_left.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_left.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_left.setFixedWidth(3)

        """
        3个功能菜单的按钮布局
        """
        self.widget_main_ui = QtWidgets.QWidget()
        self.widget_main_ui.setStyleSheet("background: rgb(255,255,255)")

        self.lay_out_main_button = QtWidgets.QVBoxLayout()

        self.lay_out_main_button.addWidget(self.button_down_text)
        self.lay_out_main_button.addWidget(self.button_format_text)
        self.lay_out_main_button.addWidget(self.button_reset_page)
        self.lay_out_main_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lay_out_main_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.lay_out_main_page = QtWidgets.QHBoxLayout(self.widget_main_ui)
        self.lay_out_main_button.setSpacing(5)
        self.lay_out_main_page.setContentsMargins(0, 5, 0, 5)
        self.lay_out_main_page.addLayout(self.lay_out_main_button)
        # self.lay_out_main_page.addWidget(self.line_left)

        """
        创建三个QWidget类型的子页面,用于存放控件
        """
        self.stack_down_param_page = QtWidgets.QWidget()  # 下载界面
        self.stack_format_page = QtWidgets.QWidget()  # 下载日志打印

        """
        创建一个堆叠容器
        """
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.stack_down_param_page)
        self.stack.addWidget(self.stack_format_page)

        """
        创建一个主窗帘布局
        """

        self.lay_out_main_ui = QtWidgets.QHBoxLayout(self)
        self.lay_out_main_ui.setContentsMargins(0, 0, 0, 0)
        self.lay_out_main_ui.addWidget(self.widget_main_ui)
        self.lay_out_main_ui.addWidget(self.stack)

        """
        下载界面控件
        """
        self.combox_select_down_type = QtWidgets.QComboBox()
        self.combox_select_down_type.addItems(["批量下载", "单章下载"])

        self.line_edit_input_website_url = QtWidgets.QTextEdit()
        self.line_edit_input_website_url.setPlaceholderText("请输入下载的url")

        self.combox_select_save_type = QtWidgets.QComboBox()
        self.combox_select_save_type.addItems(["单文件", "多文件"])

        self.button_set_save_folder = QtWidgets.QPushButton()
        self.button_set_save_folder.setText("保存目录")

        self.button_open_save_folder = QtWidgets.QPushButton()
        self.button_open_save_folder.setText("打开目录")

        self.button_execute_down_text = QtWidgets.QPushButton()
        self.button_execute_down_text.setText("开始下载")

        self.log_print = QtWidgets.QPlainTextEdit()
        self.log_print.setPlaceholderText("日志打印...")

        """
        格式化小说界面
        """
        self.manual_file_item_list = QtWidgets.QListWidget()

        self.manual_button_get_file_list = QtWidgets.QPushButton()
        self.manual_button_get_file_list.setText("打开文件")

        self.manual_button_save_file = QtWidgets.QPushButton()
        self.manual_button_save_file.setText("保存文件")

        self.manual_button_other_save_file = QtWidgets.QPushButton()
        self.manual_button_other_save_file.setText("另存为")

        self.manual_button_execute_mode = QtWidgets.QPushButton()
        self.manual_button_execute_mode.setText("开始执行")

        self.manual_comboBox_select_format_mode = QtWidgets.QComboBox()
        self.manual_comboBox_select_format_mode.addItems(["无", "换行校验", "词语纠错", "去除广告"])

        self.manual_input_select_text = QtWidgets.QLineEdit()
        self.manual_input_select_text.setPlaceholderText("请输入需要查询的内容")
        self.manual_input_replace_text = QtWidgets.QLineEdit()
        self.manual_input_replace_text.setPlaceholderText("请输入需要替换的内容")
        self.manual_button_select_text = QtWidgets.QPushButton()
        self.manual_button_select_text.setText("查询")
        self.manual_button_replace_text = QtWidgets.QPushButton()
        self.manual_button_replace_text.setText("替换")
        self.manual_button_replace_text_all = QtWidgets.QPushButton()
        self.manual_button_replace_text_all.setText("替换全部")

        self.novel_edit_print = QtWidgets.QTextEdit()
        self.novel_edit_print.setPlaceholderText("等待加载小说内容")

        """
        初始化加载
        """
        self.load_ui_main_element()
        self.load_ui_down_novel_element()
        self.load_ui_format_novel_element()

        """
        connect连接
        """
        self.button_down_text.clicked.connect(self.display_down_novel_ui)
        self.button_reset_page.clicked.connect(self.load_ui_main_element)
        self.button_format_text.clicked.connect(self.display_format_novel_ui)

    def load_ui_main_element(self):
        """
        加载主界面UI
        Pyside6 关于图片资源的加载
        https://stackoverflow.com/questions/66099225/how-can-resources-be-provided-in-pyqt6-which-has-no-pyrcc
        """
        self.setMinimumSize(300, 400)
        self.resize(300, 400)

        button_width: int = 24
        QtCore.QDir.addSearchPath('icons', 'Resource/')

        self.setWindowIcon(QtGui.QIcon('icons:file.svg'))

        self.button_down_text.setIcon(QtGui.QIcon('icons:dwonload.svg'))
        self.button_down_text.setIconSize(QtCore.QSize(button_width, button_width))
        self.button_down_text.setFlat(True)
        # self.button_down_text.setStyleSheet('background-color: transparent;')  # 移除按钮边框

        self.button_format_text.setIcon(QtGui.QIcon('icons:file.svg'))
        self.button_format_text.setIconSize(QtCore.QSize(button_width, button_width))
        self.button_format_text.setFlat(True)

        self.button_reset_page.setIcon(QtGui.QIcon('icons:reset.svg'))
        self.button_reset_page.setIconSize(QtCore.QSize(button_width, button_width))
        self.button_reset_page.setFlat(True)

        self.button_reset_page.hide()
        self.stack.hide()
        self.line_left.hide()

        self.__center()

    def load_ui_left_menu_element(self):
        """
        将按钮加载为左侧菜单栏
        :return:
        """
        self.button_reset_page.show()
        self.stack.show()
        # self.line_left.show()

    def load_ui_down_novel_element(self):
        """
        下载小说界面UI
        :return:
        """

        self.lay_out_down_novel_param = QtWidgets.QGridLayout()
        self.lay_out_down_novel_param.addWidget(self.line_edit_input_website_url, 0, 0, 2, 3)
        self.lay_out_down_novel_param.addWidget(self.button_set_save_folder, 3, 0)
        self.lay_out_down_novel_param.addWidget(self.button_open_save_folder, 3, 1)
        self.lay_out_down_novel_param.addWidget(self.button_execute_down_text, 3, 2)
        self.lay_out_down_novel_param.addWidget(self.combox_select_down_type, 4, 0)
        self.lay_out_down_novel_param.addWidget(self.combox_select_save_type, 4, 1)

        self.lay_out_down_novel = QtWidgets.QVBoxLayout()

        self.lay_out_down_novel.setSpacing(5)
        self.lay_out_down_novel.setContentsMargins(0, 5, 5, 5)
        self.lay_out_down_novel.addLayout(self.lay_out_down_novel_param)
        self.lay_out_down_novel.addWidget(self.log_print)
        self.lay_out_down_novel.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)

        self.log_print.setOverwriteMode(False)

        # 将元素加载至stack容器
        self.stack_down_param_page.setLayout(self.lay_out_down_novel)

    def load_ui_format_novel_element(self):
        """
        显示格式化小说的界面
        :return:
        """

        """
        打开文件的控件
        """
        layout_opt_file_button = QtWidgets.QGridLayout()
        layout_opt_file_button.addWidget(self.manual_button_get_file_list, 0, 0)
        layout_opt_file_button.addWidget(self.manual_button_save_file, 0, 1)
        layout_opt_file_button.addWidget(self.manual_button_other_save_file, 1, 0)

        layout_opt_format_mode_param = QtWidgets.QHBoxLayout()
        layout_opt_format_mode_param.addWidget(self.manual_comboBox_select_format_mode)
        layout_opt_format_mode_param.addWidget(self.manual_button_execute_mode)

        layout_opt_select_button = QtWidgets.QGridLayout()
        layout_opt_select_button.addWidget(self.manual_input_select_text, 0, 0, 1, 2)
        layout_opt_select_button.addWidget(self.manual_input_replace_text, 1, 0, 1, 2)
        layout_opt_select_button.addWidget(self.manual_button_select_text, 2, 0)
        layout_opt_select_button.addWidget(self.manual_button_replace_text, 2, 1)
        layout_opt_select_button.addWidget(self.manual_button_replace_text_all, 3, 0)

        """
        上下结构，加载左侧加载文件的UI
        """
        widget_format_param = QtWidgets.QWidget()
        widget_format_param.setFixedWidth(170)

        layout_opt_left_param = QtWidgets.QVBoxLayout(widget_format_param)
        layout_opt_left_param.setSpacing(5)
        layout_opt_left_param.setContentsMargins(0, 5, 5, 5)
        layout_opt_left_param.addLayout(layout_opt_file_button)
        layout_opt_left_param.addWidget(self.manual_file_item_list)
        layout_opt_left_param.addLayout(layout_opt_format_mode_param)
        layout_opt_left_param.addLayout(layout_opt_select_button)
        """
        加载右侧查询和显示内容的UI
        """
        layout_opt_right_param = QtWidgets.QVBoxLayout()
        layout_opt_right_param.addWidget(self.novel_edit_print)

        """
        加载左右param
        """

        layout_opt_format_novel = QtWidgets.QHBoxLayout()
        layout_opt_format_novel.setSpacing(5)
        layout_opt_format_novel.setContentsMargins(0, 5, 5, 5)
        layout_opt_format_novel.addWidget(widget_format_param)
        layout_opt_format_novel.addLayout(layout_opt_right_param)

        self.stack_format_page.setLayout(layout_opt_format_novel)

    def display_down_novel_ui(self):
        """
        加载下载界面
        :return:
        """
        self.setMinimumSize(300, 400)
        self.resize(300, 400)

        self.load_ui_left_menu_element()
        self.stack.setCurrentIndex(0)
        self.setWindowTitle("DownNovel")
        self.__center()

    def display_format_novel_ui(self):
        """
        加载格式化界面
        :return:
        """
        self.setMinimumSize(500, 400)
        self.resize(800, 500)

        self.load_ui_left_menu_element()
        self.stack.setCurrentIndex(1)
        self.setWindowTitle("FormatNovel")
        self.__center()

    def __center(self):
        # 获取屏幕的尺寸信息
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        # 获取窗口的尺寸信息
        size = self.geometry()
        # 将窗口移动到指定位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main_window = QLeftTabWidget()
    main_window.show()
    sys.exit(app.exec())
