import re

from PySide6.QtCore import Signal
from lxml.etree import HTML

from NovelGui.QBussinese.Bussines.GetPageContent.check_page import CheckWebSiteMode, WebsiteTemp
from NovelGui.QBussinese.RequestsCore import UABy
from NovelGui.QBussinese.RequestsCore.requestBy import request as req, ResponseHtml
from Resource.down_website_template import WebSiteTemp, WebSiteTempXpathDataClass


def check_novel_temp(html_response: HTML, xpath_temp_list: list) -> str | None:
    """
    :param html_response: 获取到的html
    :param xpath_temp_list: 需要遍历的xpath
    :return: 找到的xpath or None
    """

    if html_response is not None:
        for xpath in xpath_temp_list:
            if len(html_response.xpath(xpath)) > 0:
                return xpath
    return None


def check_page_temp(html_response: HTML) -> WebSiteTempXpathDataClass or None:
    """
    获取小说的xpath
    """
    novel_title_xpath_list: list = WebSiteTemp.novel_title_xpath.value
    novel_page_title_xpath_list: list = WebSiteTemp.novel_page_title_xpath.value
    novel_content_xpath_list: list = WebSiteTemp.novel_content_xpath.value
    next_page_name_xpath_list: list = WebSiteTemp.next_page_name_xpath.value
    next_page_url_xpath_list: list = WebSiteTemp.next_page_url_xpath.value

    novel_page_title_xpath: str = check_novel_temp(html_response=html_response,
                                                   xpath_temp_list=novel_page_title_xpath_list)
    novel_content_xpath: str = check_novel_temp(html_response=html_response, xpath_temp_list=novel_content_xpath_list)
    next_page_name_xpath: str = check_novel_temp(html_response=html_response, xpath_temp_list=next_page_name_xpath_list)
    next_page_url_xpath: str = check_novel_temp(html_response=html_response, xpath_temp_list=next_page_url_xpath_list)

    novel_title_xpath = check_novel_temp(html_response=html_response, xpath_temp_list=novel_title_xpath_list)

    if all(x is not None for x in [novel_page_title_xpath, novel_content_xpath, next_page_name_xpath,
                                   next_page_url_xpath]):
        web_temp_xpath: WebSiteTempXpathDataClass = WebSiteTempXpathDataClass(
            novel_page_name_xpath=novel_page_title_xpath,
            novel_content_xpath=novel_content_xpath,
            next_page_name_xpath=next_page_name_xpath,
            next_page_url_xpath=next_page_url_xpath,
            novel_title_xpath=novel_title_xpath)
        return web_temp_xpath
    return None


class GetPageNovel:

    def __init__(self, py_signal: Signal = None):
        """
        :param py_signal: pyside 信号
        """
        self.url_website: str = ""
        self.r = req(py_signal_str=py_signal)
        self.check_web = CheckWebSiteMode()
        self.page_content: list = []
        self.py_single = py_signal
        self.execute_status: bool = True

    def execute_single(self, execute_status: bool):
        """
        任务执行状态
        :param execute_status: True 表示执行 False 表示停止
        :return:
        """
        self.execute_status = execute_status

    def __print_single(self, content: str):
        """
        将内容打印到pyside的窗口控件
        :param content: 内容
        :return:
        """
        if self.py_single is not None:
            self.py_single.emit(content)

    def __get_website_url(self, url: str):
        """
        分析出本网站的域名
        :param url:
        :return:
        """
        if "https" in url:
            pattern: str = 'https://(.*?)/'
        else:
            pattern: str = 'http://(.*?)/'
        title_name = re.match(pattern, url)
        str_index = title_name.regs[0][1] - 1
        self.url_website = url[:str_index]
        return self.url_website

    def __get_execute_url(self, index_page_url: str, next_page_url: str):
        """
        拼接一下下一页/下一章的URL
        :param index_page_url: 当前页面执行的URL
        :param next_page_url:  下一页的URL(该URL不一定是完整的)
        """
        domain_str: str = "http"
        if "https" in index_page_url:
            domain_str = "https"
        if next_page_url.find(domain_str, 0, 5) == -1:
            count_next_url_str: int = next_page_url.count("/")
            if count_next_url_str > 0:
                left_str = next_page_url.split("/")[0]
                if left_str != "":
                    count_next_url_str = count_next_url_str + 1
            count_next_url_str = 1 if count_next_url_str == 0 else count_next_url_str
            count_index_url_str: list = [sub_str.start() for sub_str in re.finditer("/", index_page_url)]
            count_index_url_str = list(reversed(count_index_url_str))  # 反转一下，方便取值
            main_url: str = index_page_url[:count_index_url_str[count_next_url_str-1]]
            middle_str = "/" if main_url[-1:] != "/" and next_page_url[0] != "/" else ""
            next_page_url = main_url + middle_str + next_page_url
        return next_page_url

    def __save_page_content(self, content: list, file_path, file_name):
        if len(content) > 0:
            for line_content in content:
                import unicodedata
                # 去除一下不间断空符  https://www.codenong.com/cs106082416/
                line_content = unicodedata.normalize("NFKD", line_content)
                self.page_content.append(line_content.replace('\xa0', ''))  # 去除空格
        file_path = file_path + '/' if file_path[-1:] != "/" else file_path
        file = open(file_path + file_name + '.txt', "a+", encoding="utf-8")
        for i in content:
            # i = i.replace('“”', '')  # 去除这种里面没有内容的
            if "本章未完" in i or "未完待续" in i:  # 说明要翻页了，没必要存
                continue
            file.write(i)
            file.write("\r\n")
        file.close()
        self.page_content.clear()

    def get_page_data2(self, url: str, file_path: str, next_mode: bool, save_mode: bool):
        """
        获取页面内容
        :param file_path:
        :param url: 需要获取的url
        :param next_mode:
        :param save_mode:
        :return:
        """
        r_data: ResponseHtml = self.r.get(url)
        data = r_data.response_result
        if data is not None:
            self.__print_single("页面模板匹配中...")
            content_xpath = check_page_temp(data)
            if content_xpath is not None:
                self.__get_page_novel_content2(url, file_path, next_mode, save_mode,
                                               content_xpath=content_xpath)
            else:
                self.__print_single("暂不支持该网站的模式")
        else:
            if r_data.response_code == 404:
                self.__print_single("请求的URL不存在：%s" % url)
            elif r_data.response_code == 503:
                self.__print_single("该网址访问超时，请重试")
            else:
                self.__print_single("访问出错，错误码：%d" % r_data.response_code)

    def __get_page_novel_content2(self, page_url: str, file_path: str, next_mode: bool, save_mode: bool,
                                  content_xpath: WebSiteTempXpathDataClass):
        """
        获取小说内容
        :param main_url: 网址的域名
        :param page_url: 网页的URL
        :param next_mode: True，一直下载， False，只下载一章
        :param save_mode: True，单章保存, False，每个章节保存一个txt
        :param content_xpath: 页面Xpath
        :return:
        """
        index_page_url: str = page_url  # 小说第一章第一页
        next_page_url: str = ""  # 如果存在下一页/下一章的除了域名之外的路径
        page_content: list = []  # 章节内容
        novel_name: str = ""  # 小说名

        while True:
            if self.execute_status is False:
                self.__print_single("已经接受到强制终止的信号")
                break
            if next_page_url == "":
                r_data: ResponseHtml = self.r.get(index_page_url)
            else:
                next_page_url = self.__get_execute_url(index_page_url=index_page_url, next_page_url=next_page_url)
                r_data: ResponseHtml = self.r.get(url=next_page_url)
            if r_data.response_code == 200:
                """
                获取一下当前页面的内容
                """
                data: HTML = r_data.response_result

                content = data.xpath(content_xpath.novel_content_xpath)

                if len(content) == 0:
                    self.__print_single("已经全部获取完毕，即将结束")
                    break
                page_content.extend(content)

                next_page_name: str = data.xpath(content_xpath.next_page_name_xpath)[0]
                next_page_url: str = data.xpath(content_xpath.next_page_url_xpath)[0]

                page_name: str = data.xpath(content_xpath.novel_page_name_xpath)[0]
                if page_name is not None:
                    page_name = page_name.replace("\n", "").replace("\t", "")
                    page_name = page_name.strip()

                self.__print_single("已获取 %s" % page_name)

                if novel_name == "":
                    # 尝试处理一下小说名
                    # 小说名只需要获取一次就够了
                    if content_xpath.novel_title_xpath is not None:
                        novel_name: str = data.xpath(content_xpath.novel_title_xpath)[0]
                    else:
                        novel_name = "小说"
                    novel_name.strip()

                """
                处理一下章节的标题，去除一下多余的标签
                """
                page_name_list_format = re.findall(r'\(第(.*?)页\)', page_name)
                if len(page_name_list_format) > 0:
                    page_name = re.sub(r'[\r\n\u2028\u2029\s]', '', page_name, 0)
                    page_name = re.sub(r'\(第' + page_name_list_format[0] + r'页\)', '', page_name)
                end_str = [".com", ".COM", ".C0M", "C〇M", ".net", "C0m", ".comc0M", ".comC0M", ".com:C0M", ':C0M']
                for j in end_str:
                    if j in page_name:
                        page_name = page_name.replace(j, "")

                """
                开始保存获取的内容
                """
                if "下一章" in next_page_name:
                    """
                    如果当前页面有下一章的按钮，说明章姐结束，可以保存了
                    """
                    if next_mode is False:
                        # 表示下载完这一章就结束
                        self.__save_page_content(page_content, file_path, page_name)
                        break
                    if save_mode is False:
                        # 每个章节保存为一个txt
                        self.__save_page_content(page_content, file_path, page_name)
                    else:
                        # 所有内容保存为一个章姐
                        # 把标题插入到最前面
                        page_content = [page_name + "\n"] + page_content + ['\n']
                        self.__save_page_content(page_content, file_path, novel_name)
                    page_content.clear()
            elif r_data.response_code == 503:
                continue
            elif r_data.response_code == 404:
                self.__print_single("已经全部获取完毕，即将结束")
            else:
                self.__print_single("获取网页失败,错误码：%d" % r_data.response_code)
                break


if __name__ == '__main__':
    # a = get_execute_url(index_page_url="http://www.lingdxsw.com/book/60183/43107946_3.html", next_page_url="43107948.html")
    # print(a)
    GetPageNovel().get_page_data2(url="https://m.xinbanzhu.net/0_1/136067.html",
                                  file_path="/Users/luojun/Project/NovelFormatPyside6/Resource", next_mode=True,
                                  save_mode=False)
