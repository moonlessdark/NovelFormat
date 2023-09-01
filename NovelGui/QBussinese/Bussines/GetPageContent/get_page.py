import re

from PySide6.QtCore import Signal

from NovelGui.QBussinese.Bussines.GetPageContent.check_page import CheckWebSiteMode, WebsiteTemp
from NovelGui.QBussinese.RequestsCore import UABy
from NovelGui.QBussinese.RequestsCore.requestBy import request as req


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
        分析出域名
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
            if "本章未完" in i:  # 说明要翻页了，没必要存
                continue
            file.write(i)
            file.write("\r\n")
        file.close()
        self.page_content.clear()

    def get_page_data(self, url: str, file_path: str, next_mode: bool, save_mode: bool):
        """
        获取页面内容
        :param file_path:
        :param url: 需要获取的url
        :param next_mode:
        :param save_mode:
        :return:
        """
        url_main: str = self.__get_website_url(url)
        data = self.r.get(url, header=UABy.user_agent.android.value, encoding="gb18030")
        self.__print_single("页面模板匹配中...")
        web_temp: WebsiteTemp = self.check_web.check_website(data)
        if web_temp.value == WebsiteTemp.shu_bao.value:
            self.__get_page_by_shubao(url, url_main, file_path, next_mode, save_mode)
        else:
            self.__print_single("暂不支持该网站的模式")

    def __get_page_by_shubao(self, page_url: str, main_url: str, file_path: str, next_mode: bool, save_mode: bool):
        """
        获取i.shubao12.com的小说
        :param main_url: 网址的域名
        :param page_url: 网页的URL
        :param next_mode: True，一直下载， False，只下载一章
        :param save_mode: True，单章保存, False，每个章节保存一个txt
        :return:
        """
        index_page_url: str = page_url  # 小说第一章第一页
        next_page_url: str = ""  # 如果存在下一页/下一章的除了域名之外的路径
        page_name: str = ""  # 章节名词
        novel_name: str = ""  # 小说名词
        page_content: list = []  # 章节内容

        while True:
            if self.execute_status is False:
                self.__print_single("已经接受到强制终止的信号")
                break
            if next_page_url == "":
                data = self.r.get(index_page_url, header=UABy.user_agent.android.value, encoding="gb18030")
            else:
                data = self.r.get(url=main_url + str(next_page_url),
                                  header=UABy.user_agent.android.value,
                                  encoding="gb18030")
            if data is not None:
                """
                获取一下当前页面的内容
                """
                content = data.xpath("//div[@id='nr' and @class='nr_nr']/div[@id='nr1']/descendant-or-self::text()")

                if len(content) == 0:
                    self.__print_single("内容获取失败,请重新获取")
                    break
                page_content.extend(content)

                next_page_name: str = data.xpath("//a[@id='pb_next']/descendant-or-self::text()")[0]
                next_page_url: str = data.xpath("//a[@id='pb_next']/@href")[0]
                if page_name == "":
                    page_name: str = data.xpath("//div[@id='nr_title']/descendant-or-self::text()")[0]
                if novel_name == "":
                    novel_name: str = data.xpath("//div[@class='header']/h1/descendant-or-self::text()")[0]
                    novel_name.replace(" ", "")

                """
                处理一下章节的标题
                """
                page_name_list_format = re.findall(r'\(第(.*?)页\)', page_name)
                if len(page_name_list_format) > 0:
                    page_name = re.sub(r'[\r\n\u2028\u2029\s]', '', page_name, 0)
                    page_name = re.sub(r'\(第' + page_name_list_format[0] + r'页\)', '', page_name)
                    self.__print_single("正在获取 %s" % page_name)
                end_str = [".com", ".COM", ".C0M", "C〇M", ".net", "C0m", ".comc0M", ".comC0M", ".com:C0M", ':C0M']
                for j in end_str:
                    if j in page_name:
                        page_name = page_name.replace(j, "")

                """
                获取一下是否有下一页还是下一章
                """
                if "下一章" in next_page_name:
                    self.__print_single("%s 已获取,正在保存..." % page_name)
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
                    if ".html" not in next_page_url:
                        # 说明是当前的最后一章了
                        break
                    page_content.clear()
                    page_name = ""
            else:
                self.__print_single("获取网页失败")


if __name__ == '__main__':
    GetPageNovel().get_page_data(url="https://m.shubao12.xyz/1_1042/43153.html",
                                 file_path="/Users/luojun/Project/NovelFormatPyside6/Resource", next_mode=True,
                                 save_mode=False)
