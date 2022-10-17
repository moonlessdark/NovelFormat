import os
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QFileDialog
from gui.gui_th.th_download import signalThreading
from gui.gui_th.th_format import AutoFormat, ManualFormat
from gui.gui_page.novel_tools2 import Ui_Form
from novel_bussinese.Tools.FileOpt import FileOpt


class SetUI:
    def __init__(self):
        self.ui = uic.loadUi("gui/gui_page/novel_tools.ui")


class MainWindows(SetUI, Ui_Form):

    def __init__(self):
        super(MainWindows, self).__init__()

        self.down_novel_th = signalThreading()
        self.format_th = AutoFormat()
        self.format_th_manual = ManualFormat()

        # 一些元素的初始化
        self.ui.plainTextEdit.setReadOnly(True)  # 日志打印默认为只读模式

        self.save_novel_path: str = ""  # 保存爬虫获取到的小说的目录
        self.file_items_dict: dict = {}  # 手动格式化时读取的小说列表

        # 下载小说
        self.ui.pushButton.clicked.connect(self.down_novel_set_save_path)
        self.ui.button_download_start_executr.clicked.connect(self.down_novel_execute)
        # 自动格式化
        self.ui.button_format_start_execute.clicked.connect(self.format_auto_format_execute)
        self.ui.button_format_orgin_file_path.clicked.connect(self.format_auto_set_origin_file_path)
        self.ui.button_format_result_file_path.clicked.connect(self.format_auto_set_result_file_path)

        # 手动格式化
        self.ui.manual_button_get_file_list.clicked.connect(self.format_manual_get_file_items)  # 获取要处理的小说列表
        self.ui.manual_file_item_list.itemClicked.connect(
            self.format_manual_show_item_clicked_novel_content)  # 选中小说并显示内容
        self.ui.manual_button_save_file.clicked.connect(self.format_manual_save_item_clicked_novel_content)  # 保存修改的内容
        self.ui.manual_button_other_save_file.clicked.connect(self.format_manual_save_other_path)  # 文件另存为
        self.ui.manual_comboBox_select_change_line_mode.currentIndexChanged.connect(
            self.reset_select_mode_item_change_line)
        self.ui.manual_comboBox_select_format_mode.currentIndexChanged.connect(
            self.reset_select_mode_item_format)
        self.ui.manual_button_execute.clicked.connect(self.manual_execute)
        self.ui.manual_button_select_next_one.clicked.connect(self.show_error_str)

        # 线程链接
        self.down_novel_th.sin_out.connect(self.print_log)
        self.format_th.sin_out.connect(self.print_log)
        self.format_th.sin_work_status.connect(self.format_auto_button_status)
        self.down_novel_th.sin_work_status.connect(self.format_auto_button_status)

        self.format_th_manual.sin_out.connect(self.print_log)

    def print_log(self, content: str, is_clear: bool = False, is_date: bool = True, is_edit: bool = False):
        """
        打印日志
        :param is_edit: 是否允许编辑
        :param is_date: 是否显示时间
        :param is_clear: 是否清除日志
        :param content: 日志内容
        :return:
        """
        if is_clear:
            self.ui.plainTextEdit.clear()
        if is_date:
            content = str(datetime.now().strftime("%H时%M分%S秒 : ")) + content
        if is_edit:
            self.ui.plainTextEdit.setReadOnly(False)
        elif is_edit is False:
            self.ui.plainTextEdit.setReadOnly(True)
        self.ui.plainTextEdit.insertPlainText(content + '\n')

    def down_novel_set_save_path(self):
        """
        设置保存爬虫下载的小说的目录
        :return:
        """
        save_novel_path = QFileDialog.getExistingDirectory(None, '设置保存目录', os.getcwd())
        self.ui.save_novel_path_by_page.setText(save_novel_path)
        self.print_log("小说保存目录设置为：%s " % save_novel_path, is_clear=True)

    def down_novel_execute(self):
        """
        下载小说
        :return:
        """
        down_url = self.ui.input_download_url.text()
        down_mode = self.ui.select_download_mode.currentText()
        down_type = self.ui.select_download_type.currentText()
        self.down_novel_th.start_execute_init()
        if down_url == "":
            self.print_log("还未输入下载的小说URL，请输入第一页小说内容所在的URL", is_clear=True)
        elif down_mode == "":
            self.print_log("还未设置爬虫模板", is_clear=True)
        elif down_type == "":
            self.print_log("还未设置下载模式", is_clear=True)
        elif self.ui.save_novel_path_by_page.text() == "":
            self.print_log("还未设置保存的目录", is_clear=True)
        else:
            self.down_novel_th.get_param(down_url=down_url, down_mode=down_mode, down_type=down_type,
                                         save_novel_path=self.ui.save_novel_path_by_page.text() + '/')
            self.down_novel_th.start()

    def format_auto_set_origin_file_path(self):
        """
        设置格式化的源文件目录
        :return:
        """
        save_novel_path = QFileDialog.getExistingDirectory(None, '设置源文件目录', os.getcwd())
        self.ui.line_format_orgin_file_path.setText(save_novel_path + '/')
        self.print_log("源文件目录设置为：%s " % save_novel_path, is_clear=True)

    def format_auto_set_result_file_path(self):
        """
        设置格式化后的存储的目录
        :return:
        """
        save_novel_path = QFileDialog.getExistingDirectory(None, '设置结果文件目录', os.getcwd())
        self.ui.line_format_result_file_path.setText(save_novel_path + '/')
        self.print_log("结果文件目录设置为：%s " % save_novel_path, is_clear=True)

    def format_auto_format_execute(self):
        """
        格式化小说
        :return:
        """
        format_type = self.ui.select_format_type.currentText()
        format_origin_path = self.ui.line_format_orgin_file_path.text()
        format_result_path = self.ui.line_format_result_file_path.text()
        self.format_th.start_execute_init()
        if format_type == "":
            self.print_log("请选择格式化模式", is_clear=True)
        elif format_origin_path == "":
            self.print_log("请选择待处理的小说目录", is_clear=True)
        elif format_result_path == "":
            self.print_log("请选择处理结果目录", is_clear=True)
        else:
            self.ui.plainTextEdit.clear()
            self.format_th.get_param(format_mode=format_type, format_origin_path=format_origin_path,
                                     format_result_path=format_result_path)
            self.format_th.start()

    def format_auto_button_status(self, execute_status: bool):
        """
        开始执行按钮的显示状态处理
        :param execute_status: 线程是否在执行中
        :return:
        """
        if execute_status:
            self.ui.button_download_start_executr.setEnabled(False)
            self.ui.button_format_start_execute.setEnabled(False)
        else:
            self.ui.button_download_start_executr.setEnabled(True)
            self.ui.button_format_start_execute.setEnabled(True)

    def format_manual_get_file_items(self):
        """
        获取小说文件夹下的小说列表
        :return:
        """
        file_items_tuple: tuple[list[str], str] = QFileDialog.getOpenFileNames(None, "请选择需要处理的文件",
                                                                               os.getcwd(),
                                                                               "Text Files(*.txt)")
        file_items = file_items_tuple[0]
        if len(file_items) > 0:
            self.file_items_dict = {}
            self.ui.manual_file_item_list.clear()
            for i in file_items:
                i_index = i.rfind("/")
                self.file_items_dict[i[i_index + 1:]] = i[:i_index + 1]
            for key in self.file_items_dict:
                self.ui.manual_file_item_list.addItem(key)

    def format_manual_show_item_clicked_novel_content(self):
        """
        显示选中的小说
        :return:
        """
        item = self.ui.manual_file_item_list.selectedItems()[0]
        item_path: str = self.file_items_dict.get(item.text())
        file_path = item_path + item.text()
        content = FileOpt().read_file(file_path)
        self.print_log(content, True, False, True)

    def format_manual_save_item_clicked_novel_content(self):
        """
        保存已处理的小说
        :return:
        """
        content: str = self.ui.plainTextEdit.toPlainText()
        if self.ui.manual_file_item_list.selectedItems():
            item = self.ui.manual_file_item_list.selectedItems()[0]
            item_path: str = self.file_items_dict.get(item.text())
            file_path = item_path + item.text()
            with open(file_path, "w+", encoding="utf-8") as f:
                f.write(content)
                self.print_log("文件 %s 已更新" % item.text(), is_clear=True)
        else:
            self.print_log("还未选中需要保存的文件", is_clear=True)

    def format_manual_save_other_path(self):
        """
        文件另存为
        :return:
        """
        content: str = self.ui.plainTextEdit.toPlainText()
        if self.ui.manual_file_item_list.selectedItems():
            save_novel_path = QFileDialog.getExistingDirectory(None, '设置结果文件目录', os.getcwd())
            if save_novel_path != "":
                save_file_path = save_novel_path + '/' + self.ui.manual_file_item_list.selectedItems()[0].text()
                with open(save_file_path, "w+", encoding="utf-8") as f:
                    f.write(content)
                    self.print_log("文件 %s 已保存至 %s 路径下" % (self.ui.manual_file_item_list.selectedItems()[0].text(),
                                   save_novel_path), is_clear=True)
        else:
            self.print_log("还未选中需要另存的文件", is_clear=True)

    def reset_select_mode_item_format(self):
        """
        2个下拉框进行关联，选中其中一个就重置另一个
        :return:
        """
        if self.ui.manual_comboBox_select_format_mode.currentText() != "无":
            self.ui.manual_comboBox_select_change_line_mode.setCurrentIndex(0)

    def reset_select_mode_item_change_line(self):
        """
        2个下拉框进行关联，选中其中一个就重置另一个
        :return:
        """
        if self.ui.manual_comboBox_select_change_line_mode.currentText() != "无":
            self.ui.manual_comboBox_select_format_mode.setCurrentIndex(0)

    def show_error_str(self, index: int):
        """
        显示有问题的字符
        :param index: 字符下标，表示从哪里开始有异常
        :return:
        """
        show_content = self.ui.plainTextEdit
        num = show_content.document().find("老公今天特别有兴致")
        show_content.moveCursor(QTextCursor.StartOfWord("老公今天特别有兴致"))
        self.print_log("sss")

    def manual_execute(self):
        """
        开始执行手动格式化
        :return:
        """
        format_mode_str = self.ui.manual_comboBox_select_format_mode.currentText()
        content_str = self.ui.plainTextEdit.toPlainText()
        if format_mode_str != "无" and content_str != "":
            self.format_th_manual.get_param(format_mode_str, content_str)
            self.format_th_manual.start()
