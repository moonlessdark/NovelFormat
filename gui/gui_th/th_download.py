from PySide6.QtCore import QThread, QWaitCondition, QMutex, Signal

from novel_bussinese.bussines.get_page_content.get_by_shubao12.getPage import GetNovel


class SignalThreading(QThread):
    sin_out = Signal(str)
    sin_work_status = Signal(bool)
    sin_status_bar_out = Signal(str)

    def __init__(self):
        super(SignalThreading, self).__init__()

        self.working = True
        self.is_First_time = True
        self.cond = QWaitCondition()
        self.mutex = QMutex()

        self.down_url = ""
        self.down_mode = ""
        self.down_type = ""
        self.save_novel_path = ""

        self.get = GetNovel(single_str=self.sin_out, single_status_bar_str=self.sin_status_bar_out)

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

    def get_param(self, down_url: str, down_mode: str, down_type: str, save_novel_path: str):
        """
        获取一下参数
        :param down_url: 下载URL
        :param down_mode: 下载模式，即爬虫模式
        :param down_type: 单章下载或者全部下载
        :param save_novel_path: 保存的目录
        :return:
        """

        self.down_url = down_url
        self.down_mode = down_mode
        self.down_type = down_type
        self.save_novel_path = save_novel_path

    def run(self) -> None:
        while self.working:
            self.mutex.lock()
            if self.working is False:
                self.sin_work_status.emit(False)
                self.mutex.unlock()
                return None
            else:
                if self.down_type == "shubao12.com":
                    self.sin_work_status.emit(True)
                    if self.down_mode == "批量下载":
                        self.get.get_novel_by_shubao12(
                            page_url=self.down_url,
                            save_file_path=self.save_novel_path)
                    else:
                        self.sin_out.emit("单章下载模式暂未实现")
                    self.mutex.unlock()
                    self.pause()
                elif self.down_type == "tmallyh.top":
                    self.get.get_novel_by_tmallyh(url=self.down_url, save_file_path=self.save_novel_path)
                    self.mutex.unlock()
                    self.pause()
            self.sin_work_status.emit(False)
