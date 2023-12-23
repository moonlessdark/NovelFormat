from PySide6.QtCore import QThread, QWaitCondition, QMutex, Signal

from Businese.GetPageContent.req_novel_page import GetPageNovel, GetPageComic


class SignalThreading(QThread):
    sin_out = Signal(str)
    sin_work_status = Signal(bool)

    def __init__(self):
        super(SignalThreading, self).__init__()

        self.down_agent = None
        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()

        self.down_url = ""
        self.down_mode: bool = True
        self.save_type: bool = True
        self.save_novel_path = ""

        self.get = GetPageNovel(py_signal=self.sin_out)

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
        self.get.execute_single(False)
        self.sin_out.emit("已经发出停止信号,请稍后")

    def start_execute_init(self):
        """
        线程开始
        :return:
        """
        self.working = True
        self.cond.wakeAll()
        self.get.execute_single(True)

    def get_param(self, down_url: str, down_mode: str, save_type: str, save_novel_path: str, down_agent: str):
        """
        获取一下参数
        :param down_agent: 下载模式，电脑还是移动端
        :param down_url: 下载URL
        :param down_mode: 单章下载或者全部下载
        :param save_type: 保存为 “单文件”、“多文件”
        :param save_novel_path: 保存的目录
        :return:
        """
        self.down_url = down_url.replace(" ", "") if " " in down_url else down_url
        self.down_mode = True if down_mode == "批量下载" else False
        self.save_type = True if save_type == "生成单文件" else False
        self.save_novel_path = save_novel_path
        self.down_agent = down_agent

    def run(self) -> None:
        while self.working:
            self.mutex.lock()
            if self.working is False:
                self.sin_out.emit("任务已结束")
                self.sin_work_status.emit(False)
                self.mutex.unlock()
                return None
            else:
                self.sin_work_status.emit(True)
                self.get.get_page_data2(url=self.down_url, file_path=self.save_novel_path, next_mode=self.down_mode,
                                        save_mode=self.save_type, down_agent=self.down_agent)
                self.mutex.unlock()
                self.pause()
            self.sin_work_status.emit(False)


class SignalThreadingComic(QThread):
    sin_out = Signal(str)
    sin_work_status = Signal(bool)

    def __init__(self):
        super(SignalThreadingComic, self).__init__()

        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()

        self.down_url = ""
        self.save_novel_path = ""
        self.down_agent = None
        self.save_type: bool = False

        self.get = GetPageComic(py_signal=self.sin_out)

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
        self.get.execute_single(False)
        self.sin_out.emit("已经发出停止信号,请稍后")

    def start_execute_init(self):
        """
        线程开始
        :return:
        """
        self.working = True
        self.cond.wakeAll()
        self.get.execute_single(True)

    def get_param(self, down_url: str, save_novel_path: str, down_agent: str, save_type: str):
        """
        获取一下参数
        :param save_type: 生成单文件，生成多文件
                          1、如果是漫画，单文件是指打包成一个zip,多文件是放在文件夹里不打包
                          2、如果是小说，单文件是指保存到一个txt里，多文件是每个章节都保存一份单独的txt
        :param down_agent: 下载模式，电脑还是移动端
        :param down_url: 下载URL
        :param save_novel_path: 保存的目录
        :return:
        """
        self.start_execute_init()
        self.down_url = down_url.replace(" ", "") if " " in down_url else down_url
        self.save_novel_path = save_novel_path
        self.down_agent = down_agent
        self.save_type = True if save_type == "生成单文件" else False

    def run(self) -> None:
        while self.working:
            self.mutex.lock()
            if self.working is False:
                self.sin_out.emit("任务已结束")
                self.sin_work_status.emit(False)
                self.mutex.unlock()
                return None
            else:
                self.sin_work_status.emit(True)
                self.get.get_page_data(url=self.down_url, file_path=self.save_novel_path,  down_agent=self.down_agent,
                                       save_type=self.save_type)
                self.mutex.unlock()
                self.pause()
            self.sin_work_status.emit(False)
