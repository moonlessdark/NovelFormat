import re

from bussines.format_mode.common import format_common
from bussines.format_mode.global_mode import formatByGlobal2, global_mode
from bussines.format_mode.sigle_line_mode import formatByLine
from template.rexp_template import template


class executeFormat:
    """
    开始执行
    """

    def __init__(self):
        self.f = global_mode()
        self.f2 = formatByGlobal2()
        self.line = formatByLine()
        self.m = format_common()

    def star_format_global_mode(self, content_list: list) -> list:
        """
        全局检测模式1
        :param content_list:
        :return:
        """

        format_content_list = []
        if len(content_list) > 0:
            for i in content_list:
                if i != "":
                    step_2_list = self.m.wrap_by_punctuation_mark(i)  # 先统一按标点符号进行换行
                    for j in step_2_list:
                        format_content_list.append(j)
            list_2 = self.f.merge_talk(format_content_list)  # 把所有双引号中间的文案都合并到同一行，个人习惯问题
            list_3 = self.f.wrap_by_str(list_2)  # 再次判断一下双引号左右2边的文案有没有说话的动词，再来判断是不是要换行。这是因为双引号里的内容并不一定代表了说话，也可能是表示重点信息
            return list_3
        else:
            return content_list

    def star_format_global_mode2(self, content: str, title_name: str) -> list:
        """
        全局检测模式2，建议使用
        :param title_name: txt文本名称，也时章节名称
        :param content: 从txt中读取的正文内容
        :return:
        """
        format_content_list = []
        if len(content) > 0:
            r_list = self.m.format_end_2_start_double_quotation_mark(content=content, text_title_name=title_name)
            r_result = self.f2.line_feed_by_str(r_list)
            re_list = self.f2.format_end_str(r_result)
            format_content_list = self.m.line_feed_format(re_list)
        return format_content_list

    def star_format_line_mode(self, content_list: list) -> list:
        """
        检查每一行的结束是否有结束符号
        :param content_list:
        :return:
        """
        start_wrap_character = template.wrap_character_by_line.value
        result_list: list = []
        temp_str: str = ""  # 用于存放临时字符的
        for line in content_list:
            if any(wrap_str in line[-1:] for wrap_str in start_wrap_character):
                if self.m.check_line_tips(temp_str + line):
                    # result_list.append(temp_str + line)
                    # temp_str = ""
                    r_list = format_common().line_feed_format(temp_str + line)
                    for s in range(len(r_list)):
                        result_list.append(r_list[s])
                        temp_str = ""
                else:
                    temp_str = temp_str + line
            else:
                temp_str = temp_str + line
        if temp_str != "":
            # 避免出现漏网之鱼
            result_list.append(temp_str)
        return result_list

    def end_str_format(self, content_list: str):
        """
        如果这一行里面有2组双引号，那么就需要拆分一下
        :param content_list:
        :return:
        """
        for line in content_list:
            if line.count("“") > 1:
                # 说明这一行有2组以上双引号
                start_str_index: list = [substr.start() for substr in re.finditer('“', line)]
                end_str_index: list = [substr.start() for substr in re.finditer('”', line)]

                if len(start_str_index) == len(end_str_index):
                    # 说明这一行文字没有异常的双引号
                    for i in range(len(start_str_index)):
                        if any(ss in line[:start_str_index[i]] for ss in template.talk_str.value):
                            lien_split_str = line[:end_str_index[i]]
                else:
                    pass
            else:
                # 说明只有一组或没有双引号
                pass