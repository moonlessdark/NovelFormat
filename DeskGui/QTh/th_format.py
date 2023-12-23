from PySide6.QtCore import QThread, QWaitCondition, QMutex, Signal

from Businese.FormatMode.ClearAdString import ClearAd
from Businese.FormatMode.LineWrapFormat import LineWrap
from Businese.FormatMode.tradition import tradition2simple


class ManualFormat(QThread):
    """
    手动格式化
    """
    sin_out = Signal(str)
    sin_work_status = Signal(bool)
    sin_status_bar = Signal(str, bool)
    sin_out_information = Signal(str)
    sin_out_select_error_str = Signal(str)

    def __init__(self):
        super().__init__()

        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()
        # self.fm = FormatCommon(sin_out=self.sin_out_information, sin_out_status_bar=self.sin_status_bar)

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
                if self.format_mode == "换行校验":
                    self.sin_status_bar.emit("正在计算文本长度", True)
                    error_mark_str: str = LineWrap().check_novel_error_mark_str(self.content)
                    if error_mark_str != "":
                        self.sin_out_information.emit(error_mark_str)
                        self.sin_out_select_error_str.emit(error_mark_str)
                        continue
                    ye: list = LineWrap().wrap_line_by_double_quotation_mark_by_str(self.content)
                    ye: list = LineWrap().split_line_by_warp_str(ye)
                    if len(ye) == 0:
                        continue
                    content_list_format: list = LineWrap().merge_line(ye)
                    content: str = LineWrap().format_merge_list(content_list_format)
                elif self.format_mode == "去除广告":
                    content = ClearAd().clear_ad_str(self.content)
                    content = ClearAd().clear_html_code(content)
                elif self.format_mode == "词语纠错":
                    self.sin_out_information.emit("暂时不支持")
                elif self.format_mode == "繁简互换":
                    content = tradition2simple(self.content)
            except Exception as e:
                # 打印异常信息
                self.sin_out_information.emit(str(e))
            else:
                # 如果没有触发任何异常，就返回处理后的信息
                self.sin_out.emit(content)
            finally:
                self.sin_status_bar.emit("处理结束", False)
                self.working = False
                self.mutex.unlock()
