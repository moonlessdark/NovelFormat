import html
from enum import Enum


class WebsiteTemp(Enum):
    shu_bao = "https://m.shubao12.xyz"
    t_mall_yh = "tmallyh.top"


class CheckWebSiteMode:
    """
    检测网页的格式是否支持爬取内容
    """

    def check_website(self, page_content) -> WebsiteTemp:
        if self.__website_temp_shubao12(page_content):
            return WebsiteTemp.shu_bao
        elif self.____website_temp_tmallyh(page_content):
            return WebsiteTemp.t_mall_yh
        else:
            pass

    def __website_temp_shubao12(self, page_content) -> bool:
        """
        检测是否符合 shubao12.xyz 网址的网页渲染格式
        :param page_content: 获取到的网页内容
        :return:
        """
        content = page_content.xpath("//div[@id='nr' and @class='nr_nr']/div[@id='nr1']/descendant-or-self::text()")
        next_page_name = page_content.xpath("//a[@id='pb_next']/descendant-or-self::text()")
        next_page_url_list = page_content.xpath("//a[@id='pb_next']/@href")
        title_name = page_content.xpath("//div[@id='nr_title']/descendant-or-self::text()")

        if title_name != [] and content != [] and next_page_name != [] and next_page_url_list != []:
            """
            如果能获取到标题和内容  '\xa0\xa0\xa0\xa0'
            """
            # print(content[0])
            return True
        return False

    def ____website_temp_tmallyh(self, page_content) -> bool:
        """
        检测是否符合 tmallyh.top 网址的网页渲染格式
        :param page_content:
        :return:
        """
        content = page_content.xpath("//article[@class='text-body']/div/descendant-or-self::text()")
        title_name = page_content.xpath("//div[@class='content-wrap']/h1/descendant-or-self::text()")
        if title_name != [] and content != []:
            """
            如果能获取到标题和内容
            """
            return True
        return False


if __name__ == '__main__':
    from NovelGui.QBussinese.RequestsCore.requestBy import request as req
    from NovelGui.QBussinese.RequestsCore import UABy

    url: str = "https://m.shubao12.xyz/1_1042/43156.html"
    data = req().get(url=url, header=UABy.user_agent.android.value, encoding="gb18030")
    data = html.unescape(data)
    web = CheckWebSiteMode().check_website(data)
    if web.value == WebsiteTemp.t_mall_yh.value:
        print("sss")
    else:
        print("sa")
