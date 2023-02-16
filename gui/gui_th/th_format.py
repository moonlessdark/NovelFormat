from PyQt5.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal

from novel_bussinese.Tools.FileOpt import FileOpt
from novel_bussinese.Tools.textToPackage import formatContent
from novel_bussinese.bussines.action_execute.start_execute import ExecuteFormat
from novel_bussinese.bussines.format_mode.common import FormatCommon
from novel_bussinese.bussines.format_mode.global_mode import FormatByGlobal2
from novel_bussinese.bussines.format_mode.sigle_line_mode import formatByLine


class AutoFormat(QThread):
    """
    自动格式化
    """
    sin_out = pyqtSignal(str)
    sin_work_status = pyqtSignal(bool)

    def __init__(self):
        super(AutoFormat, self).__init__()

        self.fm = None

        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()

        self.format_mode = ""
        self.format_origin_path = ""
        self.format_result_path = ""

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
        self.cond.wakeAll()

    def get_param(self, format_mode: str, format_origin_path: str, format_result_path: str):
        """
        获取一下参数
        :param format_mode:
        :param format_origin_path:
        :param format_result_path:
        :return:
        """
        self.format_mode = format_mode
        self.format_origin_path = format_origin_path
        self.format_result_path = format_result_path

    def run(self):
        self.mutex.lock()
        while self.working:
            file_list: list = FileOpt.read_file_path(self.format_origin_path)
            if len(file_list) > 0:
                for i in range(len(file_list)):
                    self.sin_work_status.emit(True)
                    self.fm = FormatCommon(sin_out=self.sin_out)

                    file_path = self.format_origin_path + str(file_list[i])

                    content = FileOpt.read_file(file_path)  # 读取文件中的内容
                    content = self.fm.clear_ad_str(content)  # 清理一下广告
                    title_name: str = str(file_list[i])
                    result_content: list = []
                    ys: list = self.fm.format_end_2_start_double_quotation_mark(content=content, text_title_name=title_name)  # 先拆分2个对话之间的数据
                    if self.format_mode == "全局模式":
                        r_result = FormatByGlobal2().new_format(ys)
                        re_list = FormatByGlobal2().format_end_str(r_result)
                        result_content = self.fm.line_feed_format(re_list)
                    elif self.format_mode == "单行模式":
                        r_list = formatByLine().split_by_line_feed(content=ys, text_title_name=title_name)  # 清理换行符
                        result_content = ExecuteFormat().star_format_line_mode(r_list)
                    else:
                        self.sin_out.emit("处理模式错误，请检测代码参数是否正确")
                    FileOpt.save_txt(result_content, self.format_result_path, title_name)  # 开始保存文件
                    self.sin_out.emit("已处理： {}%  ".format(round((i + 1) / len(file_list) * 100, 2)))
            self.pause()
            self.sin_out.emit("线程已停止运行")
            self.sin_work_status.emit(False)
        self.mutex.unlock()


class ManualFormat(QThread):
    """
    手动格式化
    """
    sin_out = pyqtSignal(str, bool, bool, bool)
    sin_work_status = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()

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
                    start_index: int = FormatCommon().check_double_quotes_2(self.content)
                    # 还没写完
                elif self.format_mode == "去除广告":
                    content = FormatCommon().clear_ad_str(self.content)
                elif self.format_mode == "词语纠错":
                    pass
                elif self.format_mode == "繁转简":
                    content = FileOpt().tradition2simple(self.content)
                elif self.format_mode == "替换":
                    pass
                elif self.format_mode == "替换全部":
                    pass
            except Exception as e:
                self.sin_out.emit(str(e), True, True, True)
            else:
                self.sin_out.emit(content, True, False, True)
            finally:
                self.working = False
                self.mutex.unlock()
