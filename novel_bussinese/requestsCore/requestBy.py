# 本模块为获取页面
import random
import time

from lxml import etree
from requests import Session
from retrying import retry

from novel_bussinese.requestsCore import UABy


class request:
    """
    二次封装
    """

    def __init__(self, pyqtSignal_str=None):
        super().__init__()
        self.p = None
        self.re = Session()
        self.count_i = 0
        self.single_str = pyqtSignal_str

    @retry(stop_max_attempt_number=5, retry_on_result=None)  # 引入的第三方模块，用于失败自动重试,重试10次结束
    def get(self, url: str, proxies=None, header: UABy = UABy.user_agent.android.value, encoding: str = "utf-8"):
        """
        获取页面信息并返回
        :param encoding: utf-8 或者 gb18030
        :param header: header
        :param url: url
        :param proxies: 代理ip，string类型，传入 127.0.0.1:7890
        :return: html格式化过的页面元素
        """
        # self.p = {"https": "//127.0.0.1:7890", "http": "//127.0.0.1:7890"}
        # print("当前请求的网址为：%s" % url)
        if proxies is not None:
            if "：" in proxies:
                proxies = proxies.replace("：", ":")
            self.p = {"https://" + proxies, "http://" + proxies}

        if header is not None:
            header = {"user-agent": header}

        self.re.close()  # 避免重试时有太多连接，开始时就先关闭一下
        sleep_time = random.randint(1, 5)
        time.sleep(sleep_time)  # 稍微等待以下，减小服务器压力

        element = self.re.get(url=url, stream=True, timeout=(20, 300), headers=header, proxies=self.p)
        if element is not None:
            if element.status_code != 200:
                # print("返回的页面状态码异常:%d" % element.status_code)
                self.single_str.emit("返回的页面状态码异常:%d" % element.status_code)
                return None
            element.encoding = encoding  # 爬国内的网站，还是gb18030好使，国外就用 uft-8
            if 'text/html' in element.headers.get('Content-Type'):
                # 如果是html的，就格式化一下return
                element.content.decode(encoding, "replace")
                html_element = etree.HTML(element.text)
                # print(element.content.decode("gb18030", "replace"))
                return html_element
            else:
                # 不是网页就是文件啦，直接返回内容
                return element.content
        else:
            if element is None or element == '':
                # print("get到的content是None")
                return None
