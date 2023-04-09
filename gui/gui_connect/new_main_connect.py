import os
import time
from datetime import datetime
from time import strftime, localtime

from PyQt5 import uic
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtWidgets import QFileDialog, QStatusBar, QPlainTextEdit, QMessageBox

from gui.gui_th.th_download import SignalThreading
from gui.gui_th.th_format import ManualFormat
from novel_bussinese.Tools.FileOpt import FileOpt


class SetUI:
    def __init__(self):
        self.ui = uic.loadUi("gui/gui_page/new_main_windows2.ui")

        # 底部加一个statusbar组件，用于显示一些进度状态
        self.statusbar = QStatusBar()
        self.ui.setStatusBar(self.statusbar)
        self.statusbar.showMessage(" 等待执行")

        # 给一些元素进行初始化赋值
        self.ui.manual_input_select_text.setPlaceholderText("请输入需要查询的文字")
        self.ui.manual_input_replace_text.setPlaceholderText("请输入需要替换的文字")

        # 一些元素的初始化
        self.ui.plainTextEdit.setReadOnly(True)  # 日志打印默认为只读模式

    @staticmethod
    def print_information(error_str, message_type: QMessageBox = QMessageBox.Warning):
        """
        用于弹窗信息
        :param message_type:
        :param error_str:
        :return:
        """
        message = QMessageBox()
        # 设置消息框最小尺寸
        message.setMinimumSize(700, 200)
        message.setWindowTitle("处理信息")
        # 设置文字
        message.setText(str(error_str))
        # 设置信息性文字
        # message.setInformativeText("出现啦错误信息")
        # 控制消息框类型以改变图标
        # message.setIcon(QMessageBox.Warning)
        message.setIcon(message_type)
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        # 设置默认按钮，会被默认打开或突出显示
        message.setDefaultButton(QMessageBox.Ok)
        # 将消息框弹出，返回用户的选择
        ret = message.exec()
        if ret == QMessageBox.Ok:
            pass
        else:
            pass


class MainWindows(SetUI):

    def __init__(self):
        super(MainWindows, self).__init__()

        # 初始化一些类
        self.down_novel_th = SignalThreading()
        self.format_th_manual = ManualFormat()

        self.save_novel_path: str = ""  # 保存爬虫获取到的小说的目录
        self.file_items_dict: dict = {}  # 手动格式化时读取的小说列表

        # 下载小说
        self.ui.pushButton.clicked.connect(self.down_novel_set_save_path)  # 设置下载后的保存目录
        self.ui.button_download_start_executr.clicked.connect(self.down_novel_execute)  # 开始下载

        # 手动格式化
        self.ui.manual_button_get_file_list.clicked.connect(self.format_manual_get_file_items)  # 获取要处理的小说列表
        self.ui.manual_file_item_list.itemClicked.connect(
            self.format_manual_show_item_clicked_novel_content)  # 选中小说并显示内容
        self.ui.manual_button_save_file.clicked.connect(self.format_manual_save_item_clicked_novel_content)  # 保存修改的内容
        self.ui.manual_button_other_save_file.clicked.connect(self.format_manual_save_other_path)  # 文件另存为
        self.ui.manual_button_execute_mode.clicked.connect(self.manual_execute)  # 执行手工处理模式
        self.ui.manual_button_select_text.clicked.connect(self.manual_select_str)  # 查询文本内容
        self.ui.manual_button_replace_text.clicked.connect(self.manual_replace_str)
        self.ui.manual_button_replace_text_all.clicked.connect(self.manual_replace_str_all)

        # 线程链接
        self.down_novel_th.sin_out.connect(self.print_log)
        self.down_novel_th.sin_status_bar_out.connect(self.print_status_bar)
        self.format_th_manual.sin_out.connect(self.print_log)
        self.format_th_manual.sin_status_bar.connect(self.print_status_bar)
        self.format_th_manual.sin_out_information.connect(self.print_information)

    def print_log(self, content: str, is_clear: bool = False, is_date: bool = True, is_edit: bool = False,
                  is_line_wrap: bool = False):
        """
        打印日志
        :param is_line_wrap: 是否换行
        :param is_edit: 是否允许编辑
        :param is_date: 是否显示时间
        :param is_clear: 是否清除日志
        :param content: 日志内容
        :return:
        """
        if content != "":
            if is_clear:
                self.ui.plainTextEdit.clear()
            if is_date:
                content = str(datetime.now().strftime("%H时%M分%S秒=>")) + content
            if is_line_wrap:
                self.ui.plainTextEdit.setLineWrapMode(QPlainTextEdit.WidgetWidth)  # 日志自动换行显示
            if is_line_wrap is False:
                self.ui.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)  # 去除日志打印的自动换行
            if is_edit:
                self.ui.plainTextEdit.setReadOnly(False)
            if is_edit is False:
                self.ui.plainTextEdit.setReadOnly(True)
            self.ui.plainTextEdit.insertPlainText(content + '\n')

    def print_status_bar(self, text: str = ""):
        """
        打印底部状态栏的日志
        :param text:
        :return:
        """
        # time_str: str = strftime("%H:%M:%S", localtime())
        if text != "":
            self.statusbar.showMessage("  " + text)
        else:
            self.statusbar.showMessage("等待执行")

    def down_novel_set_save_path(self):
        """
        设置保存爬虫下载的小说的目录
        :return:
        """
        save_novel_path: str = QFileDialog.getExistingDirectory(None, '设置保存目录', os.getcwd())
        if save_novel_path != "":
            self.ui.save_novel_path_by_page.setText(save_novel_path)
            self.print_log("目录设置为：%s " % save_novel_path, is_clear=True, is_line_wrap=True, is_date=False)

    def down_novel_execute(self):
        """
        下载小说
        :return:
        """
        self.ui.plainTextEdit.clear()
        down_url = self.ui.input_download_url.text()
        down_mode = self.ui.select_download_mode.currentText()
        down_type = self.ui.select_download_type.currentText()
        self.down_novel_th.start_execute_init()
        if down_url == "":
            self.print_log("还未输入下载的小说URL，请输入第一页小说内容所在的URL", is_clear=True, is_date=False)
        elif down_mode == "":
            self.print_log("还未设置爬虫模板", is_clear=True, is_date=False)
        elif down_type == "":
            self.print_log("还未设置下载模式", is_clear=True, is_date=False)
        elif self.ui.save_novel_path_by_page.text() == "":
            self.print_log("还未设置保存的目录", is_clear=True, is_date=False)
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
        self.print_log("目录设置为：%s " % save_novel_path, is_clear=True, is_date=False)

    def format_auto_set_result_file_path(self):
        """
        设置格式化后的存储的目录
        :return:
        """
        save_novel_path = QFileDialog.getExistingDirectory(None, '设置结果文件目录', os.getcwd())
        self.ui.line_format_result_file_path.setText(save_novel_path + '/')
        self.print_log("目录设置为：%s " % save_novel_path, is_clear=True, is_date=False)

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
        self.ui.plainTextEdit.moveCursor(QTextCursor.Start)

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
                self.print_status_bar("文件 %s 已更新" % item.text())
        else:
            self.print_log("还未选中需要保存的文件", is_clear=True, is_date=False)

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
                    self.print_log(
                        "文件 %s 已保存至 %s 路径下" % (self.ui.manual_file_item_list.selectedItems()[0].text(),
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

    def manual_undo(self):
        """
        撤回上一步操作
        :return:
        """
        self.ui.plainTextEdit.undo()

    def manual_reset_select(self):
        """
        重置查询条件
        :return:
        """
        self.ui.manual_input_select_text.clear()
        self.ui.manual_input_replace_text.clear()

    def manual_select_str(self):
        """
        实现查询功能
        :return:
        """
        select_str: str = self.ui.manual_input_select_text.text()
        if select_str != "":
            search_result: bool = self.ui.plainTextEdit.find(select_str, QTextDocument.FindFlags())
            if search_result:
                self.print_status_bar("已经查询到结果")
            else:
                self.print_status_bar("没有查询到结果")

    def manual_replace_str(self):
        """
        替换信息
        # 代码参考 https://blog.csdn.net/hw5230/article/details/128907777
        :return:
        """
        select_str: str = self.ui.manual_input_select_text.text()
        replace_str: str = self.ui.manual_input_replace_text.text()
        content: str = self.ui.plainTextEdit.toPlainText()
        if select_str == "":
            self.print_information("查询条件不能为空")
        elif content == "":
            self.print_information("还未加载待处理的内容")
        else:
            selected_str: str = self.ui.plainTextEdit.textCursor().selectedText()  # 已经被光标选中的字符
            if selected_str == select_str:
                # 光标选中的的确是查询到的内容
                self.ui.plainTextEdit.insertPlainText(replace_str)
                self.print_status_bar("内容已经修改")
            else:
                self.manual_select_str()

    def manual_replace_str_all(self):
        """
        一次性替换所有
        :return:
        """
        select_str: str = self.ui.manual_input_select_text.text()
        replace_str: str = self.ui.manual_input_replace_text.text()
        content: str = self.ui.plainTextEdit.toPlainText()
        if select_str == "":
            self.print_information("查询条件不能为空")
        elif content == "":
            self.print_information("还未加载待处理的内容")
        else:
            content = content.replace(select_str, replace_str)
            self.ui.plainTextEdit.clear()
            self.ui.plainTextEdit.setPlainText(content)
            self.print_status_bar("已经全部处理完")
