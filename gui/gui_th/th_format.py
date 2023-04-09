from PyQt5.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal

from novel_bussinese.Tools.FileOpt import FileOpt
from novel_bussinese.bussines.format_mode.common import FormatCommon, WrapLine


class ManualFormat(QThread):
    """
    手动格式化
    """
    sin_out = pyqtSignal(str, bool, bool, bool)
    sin_work_status = pyqtSignal(bool)
    sin_status_bar = pyqtSignal(str)
    sin_out_information = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        self.fm = FormatCommon(sin_out=self.sin_out_information)

        self.content = ""
        self.format_mode = ""

    def __del__(self):
        # 线程状态改为和线程终止
        self.working = False
        # self.wait()

    def pause(self):
        """
        线程暂停
        :return:
        """
        self.working = False

    def start_execute_init(self):
        """
        线程开始
        :return:
        """
        self.working = True
        # self.cond.wakeAll()

    def get_param(self, format_mode: str, content: str):
        """
        获取一下参数
        :param content: 需要处理的内容
        :param format_mode: 格式化类型
        :return:
        """
        self.start_execute_init()
        self.content = content
        self.format_mode = format_mode

    def run(self) -> None:
        content = ""
        self.mutex.lock()
        while self.working:
            if self.working is False:
                return None
            try:
                self.sin_status_bar.emit("处理中,请稍后")
                if self.format_mode == "换行校验":
                    ys: list = self.fm.format_end_2_start_double_quotation_mark(content=self.content)  # 先拆分2个对话之间的数据并尝试修复双引号
                    if len(ys) == 0:
                        # 说明无法自动进行双引号修复，直接结束，需要手动修复
                        continue
                    r_list = FormatCommon().split_by_line_feed(content=ys)  # 按换行符进行切割，移除多余换行符
                    r_list = FormatCommon().split_by_end_str(r_list)  # 按照结束符再切割一次
                    content_list = WrapLine().format_str_by_end_str_for_line(r_list)
                    content = FormatCommon().format_merge_list(content_list)
                elif self.format_mode == "换行校验(增强)":
                    ys: list = self.fm.format_end_2_start_double_quotation_mark(content=self.content)  # 先拆分2个对话之间的数据
                    if len(ys) == 0:
                        # 说明无法自动进行双引号修复，直接结束，需要手动修复
                        continue
                    r_list = FormatCommon().split_by_line_feed(content=ys)  # 按换行符进行切割，移除多余换行符
                    r_list = FormatCommon().split_by_end_str(r_list)  # 按照结束符再切割一次

                elif self.format_mode == "去除广告":
                    content = FormatCommon().clear_ad_str(self.content)
                elif self.format_mode == "词语纠错":
                    pass
                elif self.format_mode == "繁转简":
                    content = FileOpt().tradition2simple(self.content)
            except Exception as e:
                # 打印异常信息
                self.sin_out_information.emit(str(e))
            else:
                # 如果没有触发任何异常，就饭后处理后的信息
                self.sin_out.emit(content, True, False, True)
            finally:
                self.sin_status_bar.emit("处理结束")
                self.working = False
                self.mutex.unlock()
