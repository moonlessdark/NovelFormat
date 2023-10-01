import dataclasses
from enum import Enum


class WebSiteTemp(Enum):
    """
    模版xpath
    """

    # 小说名
    novel_title_xpath: any = ["//div[@class='header']/h1/descendant-or-self::text()",
                              "//div[@id='book']/div[@class='path']/div[@class='p']/a[last()]/descendant-or-self::text()"]

    # 章节名
    novel_page_title_xpath: any = ["//div[@id='nr_title']/descendant-or-self::text()",
                                   "//div[@id='book']/div[@class='content']/h1/descendant-or-self::text()"]

    # 本页的正文内容
    novel_content_xpath: any = ["//div[@id='nr' and @class='nr_nr']/div[@id='nr1']/descendant-or-self::text()",
                                "//div[@id='book']/div[@class='content']/div[@id='content']/descendant-or-self::text()"]

    # 下一页/下一章（文本）
    next_page_name_xpath: any = ["//a[@id='pb_next']/descendant-or-self::text()",
                                 "//div[@id='book']/div[@class='content']/div[@class='page_chapter'][1]/ul/li[3]/a/descendant-or-self::text()"]

    # 下一页(跳转的url)
    next_page_url_xpath: any = ["//a[@id='pb_next']/@href",
                                "//div[@id='book']/div[@class='content']/div[@class='page_chapter'][1]/ul/li[3]/a/@href"]


@dataclasses.dataclass
class WebSiteTempXpathDataClass:
    novel_content_xpath: str
    next_page_name_xpath: str
    next_page_url_xpath: str
    novel_page_name_xpath: str
    novel_title_xpath: str
