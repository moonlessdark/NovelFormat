from PySide6 import QtWidgets, QtCore

from DeskGui.GuiPage.MainElement import QMainElement


class QDownSetting(QMainElement):

    def __init__(self):
        super().__init__()

        self.combox_select_down_type_label = QtWidgets.QLabel()
        self.combox_select_down_type_label.setText("请选择下载数量(仅下载小说有效)")
        self.combox_select_down_type = QtWidgets.QComboBox()
        self.combox_select_down_type.addItems(["批量下载", "单章下载"])

        self.combox_select_down_agent_label = QtWidgets.QLabel()
        self.combox_select_down_agent_label.setText("请选择模拟获取数据的浏览器。\n若未在下载界面选择请求头,则读取此配置")
        self.combox_select_down_agent = QtWidgets.QComboBox()
        # self.combox_select_down_agent.addItems(["Macos", "Windows", "Android", "IOS", "Ipad"])

        self.__load_ui_down_setting()

    def __load_ui_down_setting(self):
        """
        加载一下布局
        :return:
        """
        layout_down_setting_select_type = QtWidgets.QVBoxLayout()
        layout_down_setting_select_type.addWidget(self.combox_select_down_type_label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_down_setting_select_type.addWidget(self.combox_select_down_type, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_down_setting_select_type.setSpacing(1)
        layout_down_setting_select_type.setContentsMargins(0, 0, 0, 0)

        layout_down_setting_select_agent = QtWidgets.QVBoxLayout()
        layout_down_setting_select_agent.addWidget(self.combox_select_down_agent_label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_down_setting_select_agent.addWidget(self.combox_select_down_agent, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_down_setting_select_agent.setSpacing(1)

        down_setting = QtWidgets.QWidget(self.stack_widget_down_setting)
        layout_down_setting = QtWidgets.QVBoxLayout(down_setting)
        layout_down_setting.addLayout(layout_down_setting_select_type)
        layout_down_setting.setStretch(0, 5)
        layout_down_setting.addLayout(layout_down_setting_select_agent)
        layout_down_setting.setStretch(1, 5)
        layout_down_setting.setStretch(2, 5)
        layout_down_setting.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        layout_down_setting.setSpacing(1)
        # self.stack_widget_down_setting.setLayout(layout_down_setting)

