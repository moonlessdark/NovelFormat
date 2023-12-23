from PySide6 import QtWidgets

from DeskGui.GuiPage.MainElement import QMainElement


class QFormatNovel(QMainElement):

    def __init__(self):
        super().__init__()

        """
        格式化小说界面
        """
        self.manual_file_item_list = QtWidgets.QListWidget()

        self.manual_button_get_file_list = QtWidgets.QPushButton()
        self.manual_button_get_file_list.setText("打开")

        self.manual_button_save_file = QtWidgets.QPushButton()
        self.manual_button_save_file.setText("保存")

        self.manual_button_other_save_file = QtWidgets.QPushButton()
        self.manual_button_other_save_file.setText("另存为")

        self.manual_button_execute_mode = QtWidgets.QPushButton()
        self.manual_button_execute_mode.setText("开始执行")

        self.manual_comboBox_select_format_mode = QtWidgets.QComboBox()
        self.manual_comboBox_select_format_mode.addItems(["无", "换行校验", "去除广告", "繁简互换"])

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

        self.__load_ui_format_novel_element()

    def __load_ui_format_novel_element(self):
        """
        加载格式化的UI
        :return:
        """
        layout_opt_file_button = QtWidgets.QGridLayout()
        layout_opt_file_button.addWidget(self.manual_button_get_file_list, 0, 0)
        layout_opt_file_button.addWidget(self.manual_button_save_file, 0, 1)
        layout_opt_file_button.addWidget(self.manual_button_other_save_file, 0, 2)

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
        widget_format_param.setFixedWidth(150)

        layout_opt_left_param = QtWidgets.QVBoxLayout(widget_format_param)
        layout_opt_left_param.setSpacing(5)
        layout_opt_left_param.setContentsMargins(0, 0, 0, 0)
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
        layout_opt_format_novel.setContentsMargins(0, 0, 0, 0)
        layout_opt_format_novel.addWidget(widget_format_param)
        layout_opt_format_novel.addLayout(layout_opt_right_param)

        self.stack_widget_format_novel.setLayout(layout_opt_format_novel)
