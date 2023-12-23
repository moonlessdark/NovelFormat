# encoding: utf-8

from PySide6 import QtWidgets, QtCore, QtGui


class QMainElement(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        # self.setStyleSheet("border: 1px solid black;")

        self.is_init_size: bool = True
        self.resize(370, 470)
        self.__center()

        QtCore.QDir.addSearchPath('icons', 'Resource/icons/')
        self.setWindowIcon(QtGui.QIcon('icons:file.svg'))

        """
        主功能按钮
        """
        self.button_format_file = QtWidgets.QPushButton()
        self.button_down_content = QtWidgets.QPushButton()
        self.button_down_setting = QtWidgets.QPushButton()

        """
        创建三个QWidget类型的子页面,用于存放控件不同功能的页面元素
        """
        self.stack_widget_down_content = QtWidgets.QWidget()  # 下载小说
        self.stack_widget_down_setting = QtWidgets.QWidget()  # 下载漫画
        self.stack_widget_format_novel = QtWidgets.QWidget()  # 格式化小说

        """
        创建一个堆叠容器,用于存放不同的功能容器
        """
        self.stack_function_area = QtWidgets.QStackedWidget()
        self.stack_function_area.addWidget(self.stack_widget_down_content)
        self.stack_function_area.addWidget(self.stack_widget_format_novel)
        self.stack_function_area.addWidget(self.stack_widget_down_setting)

        self.stack_function_area.setCurrentIndex(0)

        self.__load_main_ui_layout()
        self.load_stack_down_content()

        """
        connect
        """
        self.button_down_content.clicked.connect(self.load_stack_down_content)
        self.button_format_file.clicked.connect(self.load_stack_format_novel)
        self.button_down_setting.clicked.connect(self.load_stack_down_setting)

    def __load_main_ui_layout(self):
        """
        加载主界面布局
        :return:
        """

        """
        加载左侧菜单按钮布局
        """
        menu_widget_width: int = 30

        widget_menu_button = QtWidgets.QWidget()
        widget_menu_button.setFixedWidth(menu_widget_width)

        lay_out_main_button = QtWidgets.QVBoxLayout(widget_menu_button)
        lay_out_main_button.addWidget(self.button_down_content)
        lay_out_main_button.addWidget(self.button_format_file)
        lay_out_main_button.addWidget(self.button_down_setting)
        lay_out_main_button.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        lay_out_main_button.setContentsMargins(0, 0, 0, 0)
        lay_out_main_button.setSpacing(3)

        button_width: int = menu_widget_width - 5
        self.button_down_content.setIcon(QtGui.QIcon('icons:dwonload.svg'))
        self.button_down_content.setFlat(True)
        self.button_down_content.setIconSize(QtCore.QSize(button_width, button_width))

        self.button_format_file.setIcon(QtGui.QIcon('icons:file.svg'))
        self.button_format_file.setFlat(True)
        self.button_format_file.setIconSize(QtCore.QSize(button_width, button_width))

        self.button_down_setting.setIcon(QtGui.QIcon('icons:reset.svg'))
        self.button_down_setting.setFlat(True)
        self.button_down_setting.setIconSize(QtCore.QSize(button_width, button_width))

        """
        再加载左右布局
        """
        lay_out_main_element = QtWidgets.QHBoxLayout(self)
        lay_out_main_element.addWidget(widget_menu_button)  # 占据界面的10%
        lay_out_main_element.addWidget(self.stack_function_area)  # 占据界面的90%
        lay_out_main_element.setContentsMargins(5, 5, 5, 5)
        lay_out_main_element.setSpacing(5)

    def load_stack_down_content(self):
        """
        显示下载界面stack容器
        :return:
        """
        self.setMinimumSize(370, 470)
        self.resize(370, 470)
        self.__center()
        self.stack_function_area.setCurrentIndex(0)

    def load_stack_format_novel(self):
        """
        显示格式化小说的界面stack容器
        :return:
        """
        self.setMinimumSize(650, 470)
        self.resize(650, 470)
        self.__center()
        self.stack_function_area.setCurrentIndex(1)

    def load_stack_down_setting(self):
        """
        显示下载设置界面stack容器
        :return:
        """
        self.setMinimumSize(370, 470)
        self.resize(370, 470)
        self.__center()
        self.stack_function_area.setCurrentIndex(2)

    def __center(self):
        # 获取屏幕的尺寸信息
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        # 获取窗口的尺寸信息
        size = self.geometry()
        # 将窗口移动到指定位置
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

