import re
from novel_bussinese.Tools.FileOpt import FileOpt
from novel_bussinese.requestsCore import UABy
from novel_bussinese.requestsCore.requestBy import request as req


class getNovel:

    def __init__(self, single_str, single_status_bar_str):
        """
        信号槽
        :param single_str: 日志打印信号槽对象
        :param single_status_bar_str: 状态栏信号槽对象
        """
        super(getNovel, self).__init__()
        self.single_str = single_str
        self.single_status_bar_str = single_status_bar_str
        self.r = req(pyqtSignal_str=single_status_bar_str)

    @staticmethod
    def get_page_num(url: str) -> str:
        """
        获取当前页面是该章节的第几页
        :param url: url
        :return: 页码数
        """
        url = url[url.rfind("/") + 1:]
        index_num = url.rfind("_")
        if index_num > 0:
            return str(url[index_num + 1:url.rfind(".html")])
        else:
            return str(1)

    def get_novel_by_shubao12(self, page_url, save_file_path):
        """
        获取i.shubao12.com的小说
        :param page_url:
        :param save_file_path:
        :return:
        """
        index_page_url = page_url  # 小说第一章第一页
        file_path = save_file_path  # 存放的文件夹
        next_page_url = None
        title_name_str = ""
        while True:
            self.single_status_bar_str.emit("准备获取页面")
            if "shubao" not in page_url:
                self.single_str.emit("下载网站不匹配，请重新选择")
                break
            if title_name_str == "":
                self.single_str.emit("开始下载")
            if next_page_url is None:
                data = self.r.get(index_page_url, header=UABy.user_agent.android.value, encoding="gb18030")
                self.single_status_bar_str.emit("正在处理该章节的第 1 页")
            else:
                data = self.r.get("https://i.shubao12.cc/" + str(next_page_url), header=UABy.user_agent.android.value,
                                  encoding="gb18030")
                self.single_status_bar_str.emit("正在处理该章节的第 %s 页" % self.get_page_num(next_page_url))
            if data is not None:
                content = data.xpath("//div[@id='nr' and @class='nr_nr']/div[@id='nr1']/descendant-or-self::text()")
                next_page_name = data.xpath("//a[@id='pb_next']/descendant-or-self::text()")
                next_page_url_list = data.xpath("//a[@id='pb_next']/@href")
                title_name = data.xpath("//div[@id='nr_title']/descendant-or-self::text()")
                try:
                    title_name = title_name[0]
                except Exception:
                    self.single_str.emit("全部章节已经下载完成")
                    break
                title_name_list = re.findall('\(第(.*?)页\)', title_name)
                if len(title_name_list) > 0:
                    title_name = re.sub('[\r\n\u2028\u2029\s]', '', title_name, 0)
                    title_name = re.sub('\(第' + title_name_list[0] + '页\)', '', title_name)

                if title_name != title_name_str:
                    self.single_str.emit("开始下载 %s" % title_name)
                    title_name_str = title_name

                if "下一页" or "下一章" in next_page_name:
                    if len(next_page_url_list) == 0:
                        break
                    next_page_url = next_page_url_list[0]
                    end_str = [".com", ".COM", ".C0M", "C〇M", ".net", "C0m", ".comc0M", ".comC0M", ".com:C0M", ':C0M']
                    for j in end_str:
                        if j in title_name:
                            title_name = title_name.replace(j, "")
                    file_name = file_path + title_name
                    file = open(file_name + ".txt", "a+", encoding="utf-8")
                    for i in content:
                        i = i.replace('\xa0', '')  # 去除空格
                        i = i.replace('“”', '')  # 去除这种里面没有内容的
                        if "本章未完" in i:  # 说明要翻页了，没必要存
                            continue
                        file.write(i)
                        file.write("\r\n")
                    file.close()
                    # self.single_status_bar_str.emit("等待执行")
                else:
                    self.single_str.emit("全部章节已经下载完成")
                    # print("文章都下载下来了")
                    break
            else:
                self.single_str.emit("小说下载失败，已终止")
                # print("小说下载失败，已终止")
                break

    def get_novel_by_tmallyh(self, url: str, save_file_path: str):
        """
        获取tmallyh.top的小说
        :param save_file_path:
        :param url:
        :return:
        """
        self.single_str.emit("开始处理")
        self.single_status_bar_str.emit("正在处理该章节的第 1 页")
        data = self.r.get(url, header=UABy.user_agent.chrome_macos.value, encoding="utf-8")
        if data is not None:
            content = data.xpath("//article[@class='text-body']/div/descendant-or-self::text()")
            title_name = data.xpath("//div[@class='content-wrap']/h1/descendant-or-self::text()")
            title_names = ""
            for i in title_name:
                title_names = title_names + i

            FileOpt().save_txt(content=content, text_path=save_file_path, text_name=title_names)
            self.single_str.emit("该章节已下载完成")
            self.single_status_bar_str.emit("等待执行")
        else:
            self.single_str.emit("小说下载失败，已终止")