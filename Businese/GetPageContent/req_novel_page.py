import datetime
import os
import re
import zipfile

from PySide6.QtCore import Signal
from lxml.etree import HTML

from Common.RequestsCore.requestBy import RequestBy as req, ResponseHtml
from Businese.FormatMode.NovelString import ReadNovelString, WebSiteNovelTempXpathDataClass, ReadComicString, \
    WebSiteComicTempXpathDataClass


def hit_novel_xpath_temp(html_response: HTML, xpath_temp_list: list) -> str | None:
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


def get_novel_template(html_response: HTML):
    """
    获取小说模板
    :param html_response:
    :return:
    """
    website_json = ReadNovelString().get_website_json()
    website_temp: dict = website_json.get("WebSiteTemp")
    novel_page_title_xpath: str = hit_novel_xpath_temp(html_response=html_response,
                                                       xpath_temp_list=website_temp.get("novelPageTitleXpath"))
    novel_content_xpath: str = hit_novel_xpath_temp(html_response=html_response,
                                                    xpath_temp_list=website_temp.get("novelContentXpath"))
    next_page_name_xpath: str = hit_novel_xpath_temp(html_response=html_response,
                                                     xpath_temp_list=website_temp.get("nextPageNameXpath"))
    next_page_url_xpath: str = hit_novel_xpath_temp(html_response=html_response,
                                                    xpath_temp_list=website_temp.get("nextPageUrlXpath"))
    novel_title_xpath: str = hit_novel_xpath_temp(html_response=html_response,
                                                  xpath_temp_list=website_temp.get("novelTitleXpath"))

    if all(x is not None for x in
           [novel_page_title_xpath, novel_content_xpath, next_page_name_xpath, next_page_url_xpath]):
        web_temp_xpath: WebSiteNovelTempXpathDataClass = WebSiteNovelTempXpathDataClass(
            novel_page_name_xpath=novel_page_title_xpath,
            novel_content_xpath=novel_content_xpath,
            next_page_name_xpath=next_page_name_xpath,
            next_page_url_xpath=next_page_url_xpath,
            novel_title_xpath=novel_title_xpath)
        return web_temp_xpath
    return None


def get_comic_template(html_response: HTML):
    """
    匹配漫画的模板
    :param html_response:
    :return:
    """
    website_json = ReadComicString().get_website_json()
    website_temp: dict = website_json.get("WebSiteTemp")
    comic_content_xpath: str = hit_novel_xpath_temp(html_response=html_response,
                                                    xpath_temp_list=website_temp.get("comicContentXpath"))
    next_page_url_xpath: str = hit_novel_xpath_temp(html_response=html_response,
                                                    xpath_temp_list=website_temp.get("nextPageUrlXpath"))

    if all(x is not None for x in [comic_content_xpath, next_page_url_xpath]):
        web_temp_xpath: WebSiteComicTempXpathDataClass = WebSiteComicTempXpathDataClass(
            comic_content_xpath=comic_content_xpath,
            next_page_url_xpath=next_page_url_xpath)
        return web_temp_xpath
    return None


class GetPageNovel:

    def __init__(self, py_signal: Signal = None):
        """
        :param py_signal: pyside 信号
        """
        self.url_website: str = ""
        self.r = req(py_signal_str=py_signal)
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

    @staticmethod
    def __get_execute_url(index_page_url: str, next_page_url: str):
        """
        拼接一下下一页/下一章的URL
        :param index_page_url: 当前页面执行的URL
        :param next_page_url:  下一页的URL(该URL不一定是完整的)
        """
        domain_str = "https" if "https" in index_page_url else "http"

        if next_page_url.find(domain_str, 0, 5) == -1:
            count_next_url_str: int = next_page_url.count("/")
            if count_next_url_str > 0:
                left_str = next_page_url.split("/")[0]
                if left_str != "":
                    count_next_url_str = count_next_url_str + 1
            count_next_url_str = 1 if count_next_url_str == 0 else count_next_url_str
            count_index_url_str: list = [sub_str.start() for sub_str in re.finditer("/", index_page_url)]
            count_index_url_str = list(reversed(count_index_url_str))  # 反转一下，方便取值
            main_url: str = index_page_url[:count_index_url_str[count_next_url_str - 1]]
            middle_str = "/" if main_url[-1:] != "/" and next_page_url[0] != "/" else ""
            next_page_url = main_url + middle_str + next_page_url
        return next_page_url

    def __save_page_content(self, content: list, file_path, file_name):
        """
        保存页面获取的小说内容
        :param content:
        :param file_path:
        :param file_name:
        :return:
        """
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

    def get_page_data2(self, url: str, file_path: str, next_mode: bool, save_mode: bool, down_agent: str or dict):
        """
        获取页面内容
        :param down_agent:
        :param file_path:
        :param url: 需要获取的url
        :param next_mode:
        :param save_mode:
        :return:
        """

        r_data: ResponseHtml = self.r.get(url=url, header=down_agent)
        data = r_data.response_result
        if data is not None:
            self.__print_single("页面模板匹配中...")
            content_xpath = get_novel_template(data)
            if content_xpath is not None:
                self.__get_page_novel_content2(url, file_path, next_mode, save_mode,
                                               content_xpath=content_xpath, down_agent=down_agent)
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
                                  content_xpath: WebSiteNovelTempXpathDataClass, down_agent: str):
        """
        获取小说内容
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
                r_data: ResponseHtml = self.r.get(url=index_page_url, header=down_agent)
            else:
                next_page_url = self.__get_execute_url(index_page_url=index_page_url, next_page_url=next_page_url)
                r_data: ResponseHtml = self.r.get(url=next_page_url, header=down_agent)
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
                break
            else:
                self.__print_single("获取网页失败,错误码：%d" % r_data.response_code)
                break


class GetPageComic:

    def __init__(self, py_signal: Signal = None):
        """
        :param py_signal: pyside 信号
        """
        self.url_website: str = ""
        self.r = req(py_signal_str=py_signal)
        self.page_content: list = []
        self.py_single = py_signal
        self.execute_status: bool = True

    def __print_single(self, content: str):
        """
        将内容打印到pyside的窗口控件
        :param content: 内容
        :return:
        """
        if self.py_single is not None:
            self.py_single.emit(content)

    def execute_single(self, execute_status: bool):
        """
        任务执行状态
        :param execute_status: True 表示执行 False 表示停止
        :return:
        """
        self.execute_status = execute_status

    @staticmethod
    def __save_comic(save_path: str, file_name_str: str, pic_content: bytes):
        """
        保存图片
        :param save_path:
        :param file_name_str:
        :param pic_content:
        :return:
        """
        if os.path.exists(save_path) is False:
            # 新建多级目录，如果是新增单级目录，用os.mkdir()
            os.makedirs(save_path)
        with open(save_path + "/" + str(file_name_str), "wb") as f:
            f.write(pic_content)
            f.close()

    @staticmethod
    def __zip_file(save_path: str, file_name_str: str):
        """
        将文件打包为Zip
        :param save_path:
        :param file_name_str:
        :return:
        """
        # 新增一个zip文件
        zip_file = zipfile.ZipFile(save_path + file_name_str + ".zip", "w")
        for root, file_name, filenames in os.walk(save_path + file_name_str):
            fpath = root.replace(save_path, '')  # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and (fpath + os.sep) or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                zip_file.write(os.path.join(save_path + file_name_str + "/", filename), fpath + filename)
        zip_file.close()

    @staticmethod
    def __format_next_req_url(index_page_url: str, next_page_url: str):
        """
        拼接一下下一页/下一章的URL
        :param index_page_url: 当前页面执行的URL
        :param next_page_url:  下一页的URL(该URL不一定是完整的)
        """
        domain_str = "https" if "https" in index_page_url else "http"

        if next_page_url.find(domain_str, 0, 5) == -1:
            """
            如果在传入的下一页的url中没有找到 http 或者 https，那么就来给他拼接一下
            """
            count_next_url_str: int = next_page_url.count("/")
            if count_next_url_str > 0:
                left_str = next_page_url.split("/")[0]
                if left_str != "":
                    count_next_url_str = count_next_url_str + 1
            count_next_url_str = 1 if count_next_url_str == 0 else count_next_url_str
            count_index_url_str: list = [sub_str.start() for sub_str in re.finditer("/", index_page_url)]
            count_index_url_str = list(reversed(count_index_url_str))  # 反转一下，方便取值
            main_url: str = index_page_url[:count_index_url_str[count_next_url_str - 1]]
            middle_str = "/" if main_url[-1:] != "/" and next_page_url[0] != "/" else ""
            next_page_url = main_url + middle_str + next_page_url
        return next_page_url

    def __get_page_comic_content(self, url: str, file_path: str, content_xpath: WebSiteComicTempXpathDataClass,
                                 down_agent: str or dict, save_type: bool):
        """
        保存漫画
        :param url:
        :param file_path:
        :param content_xpath:
        :param down_agent:
        :param save_type:
        :return:
        """
        current_time = datetime.datetime.now()
        file_path = file_path + "/ComicTemp/"
        file_folder = current_time.strftime("%H_%M_%S")
        while 1:
            pic_content_is_get: bool = False
            res: ResponseHtml = self.r.get(url=url, header=down_agent)
            if res.response_code == 200:
                # 获取本页的图片url
                pic_content_scr_url: str = res.response_result.xpath(content_xpath.comic_content_xpath)[0]
                # 获取图片
                pic_content_res = self.r.get(url=pic_content_scr_url, header=down_agent)
                if pic_content_res.response_code == 200:
                    r_index: int = pic_content_scr_url.rfind("/")
                    file_name_str: str = pic_content_scr_url[r_index + 1:]
                    self.__print_single("正在获取漫画图片 %s" % file_name_str)
                    self.__save_comic(file_path+file_folder, file_name_str, pic_content_res.response_result)
                    pic_content_is_get = True
                if pic_content_is_get:
                    # 获取一下下一页的 url
                    next_href_url: str = res.response_result.xpath(content_xpath.next_page_url_xpath)[0]
                    if next_href_url.count("/") == 4:
                        url = self.__format_next_req_url(url, next_href_url)
                    else:
                        self.__print_single("漫画获取完毕")
                        break
            else:
                self.__print_single("漫画获取完毕")
                break
        if save_type:
            self.__zip_file(file_path, file_folder)

    def get_page_data(self, url: str, file_path: str, down_agent: str or dict, save_type: bool):
        """
        获取页面内容
        :param save_type:
        :param down_agent:
        :param file_path:
        :param url: 需要获取的url
        :return:
        """

        r_data: ResponseHtml = self.r.get(url=url, header=down_agent)
        data = r_data.response_result
        if data is not None:
            self.__print_single("页面模板匹配中...")
            content_xpath = get_comic_template(data)
            if content_xpath is not None:
                self.__get_page_comic_content(url, file_path, content_xpath=content_xpath, down_agent=down_agent,
                                              save_type=save_type)
            else:
                self.__print_single("暂不支持该网站的模式")
        else:
            if r_data.response_code == 403:
                self.__print_single("CSRF Token Invalid,错误码：%s，请手动刷新页面检查是否触发了人机校验" % url)
            elif r_data.response_code == 404:
                self.__print_single("请求的URL不存在：%s" % url)
            elif r_data.response_code == 503:
                self.__print_single("该网址访问超时，请重试")
            else:
                self.__print_single("访问出错，错误码：%d" % r_data.response_code)
