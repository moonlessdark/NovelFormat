import re

from Tools.textToPackage import *


class formatByRule():
    """
    通过正则格式化小说内容
    """

    def __init__(self):
        self.fc = formatContent()

    @staticmethod
    def format_double_quotation_mark(content: str) -> list:
        """
        双引号进行切割数组，形式为  "xxxx"<换行>
        :param content:
        :return:
        """
        a = re.findall('“([^“]*)”', content)
        if len(a) > 0:
            for i in a:
                content = re.sub(i + '”', i + '”'"\\n", content)
        content_list = content.split("\n")
        return content_list

    @staticmethod
    def format_end_2_start_double_quotation_mark(content: str) -> list:
        """
        结束双引号和开始双引号之间  例如， “xxxx”<换行>"xxxx"
        :param content:
        :return:
        """
        a = re.findall("”“", content)
        if len(a) > 0:
            content = re.sub('”“', '”\\n“', content)
            content_list = content.split("\n")
            return content_list
        else:
            return [content]

    def wrap_by_double_quotation_mark(self, content: str) -> list:
        """
        检查2句对话中间的句子里有没有标识符可以进行换行
        如果纯在可以判断换行的标识符，那就在这些标识符后面进行换行
        如果不存在换行标识符，就检查是否存在不允许换行的特殊字符，如果没有，就整句换行
        :param content:
        :return:
        """
        change_line_str = ["。", "？", "！"]
        result = re.findall("”(.*?)“", content)
        if len(result) > 0:
            for i in range(len(result)):
                str_bool = False
                is_split_not = 0
                split_string = result[i]
                sa = content.split(split_string)
                if len(sa) == 2:
                    left_str = sa[0]
                    right_str = sa[1]
                else:
                    ah = self.fc.remake_content_list(content=content, split_str=split_string)
                    left_str = ah[0]
                    right_str = ah[1]
                temp_str = result[i]
                for n in change_line_str:  # 循环一下标点符号
                    if n in temp_str:
                        str_bool = True
                        temp_str = re.sub(n, n + "\\n", temp_str)
                if str_bool is True:
                    """
                    存在换行符，开始换行
                    """
                    content = left_str + temp_str + right_str
                elif str_bool is False:
                    """
                    如果str里面没有特定的标点符号，那么执行以下操作
                    """
                    str_not_split = ['了一声', '了一句', '的', '都']
                    for x in str_not_split:
                        if split_string.find(x) != 0:
                            """
                            不是以数组里的字符开头的话，就可以正常换行
                            """
                            is_split_not += 1
                    if is_split_not == len(str_not_split):
                        """
                        不能换行的字符，都不存在，那么这一行就可以加换行符了
                        """
                        a = split_string + right_str
                        content = content.replace(a, "\n" + a)
        return content.split("\n")


    @staticmethod
    def format_end_str(content: str) -> list:
        """
        检查双引号后面的数据，到句号为止，其中有么有以下关键字。有的话就句号后面换行，没有就引号后面换行
        :param content:
        :return:
        """
        end_str = ["说道", "嘀咕", "笑骂", "怒骂", "骂道", "碎碎念", "大吼", "大叫", "笑道", "嘟囔", "揶揄道", "问道"]
        result = re.findall("”(.*?)。", content)
        end_bool = False

        # print(content)
        if len(result) > 0:
            for i in result:
                if i != "":
                    split_result = content.split(i)
                    left_results = split_result[0]
                    try:
                        right_results = split_result[1]
                    except Exception as e:
                        print("数组越界")
                    if "“" in i:
                        if "了一声" not in i:
                            n = re.sub("”", "”\\n", i)
                            content = left_results + n + right_results
                        else:
                            temp_str = i + right_results
                            content = re.sub(temp_str, "\\n" + temp_str, content)
                    else:
                        for n in end_str:
                            if n in i:
                                k = re.sub("。", "。\\n", i)
                                content = left_results + k + right_results
                                end_bool = True
                                break
                        if end_bool is False:
                            temp_str = i + right_results
                            try:
                                content = re.sub(temp_str, "\\n" + temp_str, content)
                            except Exception:
                                print("sss")
        return content.split("\n")

    @staticmethod
    def format_start_str(content) -> list:
        """
        双引号左侧的数据，如果有以下标识符，就换行
        :param content:
        :return:
        """
        change_line_str = ["。", "？", "！"]
        while True:
            result = re.findall("(.*?)“", content)
            # result = content.split("“")
            if len(result) > 0:
                for i in result:
                    if i != "":
                        split_result = content.split(i)
                        left_result = split_result[0]
                        try:
                            right_result = split_result[1]
                        except Exception:
                            print("数组越界了")
                        if "了一声" not in i:
                            if "”" in i:
                                n = re.sub("”", "”\\n", i)
                                content = left_result + n + right_result
                            else:
                                for m in change_line_str:
                                    if m in i:
                                        i = re.sub(m, m + "\\n", i)
                                content = left_result + i + right_result
            else:
                content_list_by_ju = re.sub("。", "。\\n", content)
                str_content = ""
                for s in content_list_by_ju:
                    str_content = str_content + s
                content = str_content
            return content.split("\n")

    def wrap_by_punctuation_mark(self, content: str) -> list:
        """
        按照标点符号进行换行
        :param content:
        :return:
        """
        change_line_str = ["。", "？", "！"]  # 如果碰到这个标点符号，就换行

        for i in change_line_str:
            if i != '':
                content_change = re.sub(i, i+'\n', content)
                content_list = content_change.split("\n")
                content = ""
                for n in range(len(content_list)):
                    if content_list[n][0:1] != "”":
                        content = content + '\n' + content_list[n]
                    else:
                        content = content + content_list[n]
        return content.split('\n')

    def merge_talk(self, content: list) -> list:
        """
        将双引号中的所有内容重新拼接为一行显示
        :param content:
        :return:
        """
        content_str = ""
        is_end = False
        is_start = False
        for h in content:
            if h != '':
                if "“" in h and '”' not in h:
                    is_start = True
                    is_end = False
                    content_str = content_str + h
                elif "“" not in h and '”' in h:
                    content_str = content_str + h + '\n'
                    is_end = True
                else:
                    if is_start is False:
                        content_str = content_str + h + '\n'
                    else:
                        if is_end is True:
                            content_str = content_str + '\n' + h + '\n'
                            is_start = False
                        else:
                            content_str = content_str + h
        return content_str.split('\n')

    def wrap_by_str(self, content: list)-> list:
        """
        一行文字中，双引号左右2边都有内容的进行判断，检查是前面还是后面需要换行。
        :param content:
        :return:
        """
        end_str = ['：', "说道", "嘀咕", "笑骂", "怒骂", "骂道", "碎碎念", "大吼", "大叫", "笑道", "嘟囔", "揶揄", "问道", '呵斥', '边唱', '边说']
        line_content_str = ""
        for l in content:
            if l != '':
                change_line_left = False
                change_line_right = False
                l_list_left = l.split('“')
                l_list_right = l.split('”')
                if len(l_list_left) > 2:
                    line = re.sub('”', '”'+'\n', l)
                    line_split = line.split('\n')
                    for s in line_split:
                        for e in end_str:
                            if e in s:
                                change_line_left = True
                                continue
                        if change_line_left is True:
                            line_content_str = line_content_str + s + '\n'
                        else:
                            line_content_str = line_content_str + s
                elif len(l_list_left) == 2:
                    if l_list_left[0] != '':
                        """
                        检查对话左侧的数据
                        """
                        for e in end_str:
                            if e in l_list_left[0]:
                                change_line_left = True
                                continue
                    if l_list_right[1] != '':
                        for e in end_str:
                            if e in l_list_right[1]:
                                change_line_right = True
                                continue
                    if change_line_left is True and change_line_right is False:
                        line_str = l.replace('”', '”'+'\n')
                        line_content_str = line_content_str + line_str + '\n'
                    elif change_line_left is False and change_line_right is True:
                        line_str = l.replace('“', '\n' + '“')
                        line_content_str = line_content_str + line_str + '\n'
                    else:
                        line_content_str = line_content_str + l + '\n'
                else:
                    line_content_str = line_content_str + l + '\n'
        return line_content_str.split('\n')
