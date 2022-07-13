# encoding: utf-8
import re

from template.rexp_template import template


class format_common:

    def __init__(self):
        """
        全局模式和单行模式公用的一些方法
        """
        self.ad_str_tuple = template.ad_str.value

    def clear_ad_str(self, content: str) -> str:
        """
        去除广告, 去除固定的以某个字符串开头+某个字符串结尾的广告
        :param content:
        :return:
        """
        if len(self.ad_str_tuple) > 0:
            for ad_num in self.ad_str_tuple:
                start = ad_num[0]
                end = ad_num[1]
                rex = start + '(.*?)' + end
                result = re.findall(rex, content)
                if len(result) > 0:
                    for ad_str in range(len(result)):
                        if ad_str != '':
                            replace_str = start + str(result[ad_str]) + end
                            if '\\' in replace_str:
                                replace_str = replace_str.replace('\\', '')
                            content = content.replace(replace_str, '')
        return content

    def format_end_2_start_double_quotation_mark(self, content: str, text_title_name: str = None,
                                                 is_fix_quotation_mark=True) -> list:
        """
        检查双引号和开始双引号之间  例如， “xxxx”<换行>"xxxx"
        :param is_fix_quotation_mark: 是否尝试修复文本中的异常双引号
        :param text_title_name: 文章名称，用于打印检查到异常双引号号时的信息print信息
        :param content: 文章正文
        :return:
        """
        content = self.clear_ad_str(content)
        if is_fix_quotation_mark:
            content = self.check_double_quotes(content=content, text_title_name=text_title_name)
        a = re.findall("”“", content)
        b = []
        if len(a) > 0:
            content = re.sub('”“', '”\\n“', content)
            content_list = content.split("\n")
            for ss in range(len(content_list)):
                if content_list[ss] != "":
                    b.append(content_list[ss])
            return b
        else:
            return [content]

    def fix_double_quotes_check(self, content: str):
        """
        尝试修复异常的双引号
        :param content: 正文内容
        :return:
        """
        start_str = '“'  # 开始双引号
        end_str = '”'  # 结束双引号

        left_list = [substr.start() for substr in re.finditer(start_str, content)]  # 查询开始字符串所有的index
        right_list = [substr.start() for substr in re.finditer(end_str, content)]  # 查询结束字符串所有的index
        temp_list: list = left_list  # 拼接一下
        temp_list.extend(right_list)
        temp_list.sort()  # 按照从小到大排序

        if len(temp_list) % 2 != 0:  # 说明不是偶数，出现了多余的双引号
            print("出现了多余的双引号，自动处理会出现较大的误差，如效果不佳请手动处理")

        for i in range(len(temp_list) - 1):
            if len(temp_list) == i + 1:
                # 如果此时已经循环到最后一个了，
                break
            if i % 2 != 0:
                continue
            left = temp_list[i]
            right = temp_list[i + 1]
            if content[left] == start_str and content[right] == end_str:
                """
                第一个字符串是开始，第二个字符串是结束
                """
                continue
            else:
                if content[left] != start_str:
                    string_list = list(content)
                    string_list[left] = start_str
                    content = ''.join(string_list)
                if content[right] != end_str:
                    string_list = list(content)
                    string_list[right] = end_str
                    content = ''.join(string_list)

        return content

    def check_double_quotes(self, content: str, text_title_name: str, is_fix_double_quotes: bool = True):
        """
        检查双引号是否正确
        :param is_fix_double_quotes: 是否尝试修复异常双引号
        :param content: 正文内容
        :param text_title_name: 文本标题，用于出错时打印信息
        :return:
        """
        start_str = '“'  # 开始双引号
        end_str = '”'  # 结束双引号

        left_list = [substr.start() for substr in re.finditer(start_str, content)]  # 查询开始字符串所有的index
        right_list = [substr.start() for substr in re.finditer(end_str, content)]  # 查询结束字符串所有的index

        sort_list: list = left_list if len(left_list) < len(right_list) else right_list  # 看看哪个数组更短
        if len(left_list) != len(right_list):
            for i in range(len(sort_list) - 1):
                if left_list[i] < right_list[i] < left_list[i + 1]:  # 再检查一次，确认所有的字符排序都是正常的。
                    continue
                else:
                    print("该章节_" + text_title_name + "_从内容 " + content[left_list[i]:left_list[i] + 20] + "......开始"
                          "出现双引号异常的情况，如此处的换行效果不佳，请手动处理后重新格式化")
                    if is_fix_double_quotes:
                        return self.fix_double_quotes_check(content)
        return content

    def fix_double_quotes(self, content: str, text_title_name: str = None) -> str:
        """
        检查双引号是否存在异常使用的情况。并尝试修复(不推荐使用)
        :param text_title_name: 章节名，用于打印提示信息
        :param content: 文本内容
        :return:
        """
        start_str = '“'  # 开始双引号
        end_str = '”'  # 结束双引号

        left_list = [substr.start() for substr in re.finditer(start_str, content)]  # 查询开始字符串所有的index
        right_list = [substr.start() for substr in re.finditer(end_str, content)]  # 查询结束字符串所有的index

        left_list.extend(right_list)
        left_list.sort()  # 按照从小到大排序

        if len(left_list) % 2 == 0:  # 说明是个偶数
            for i in range(len(left_list)):
                if len(left_list) == i + 1:
                    # 如果此时已经循环到最后一个了，
                    break
                if i % 2 != 0:
                    continue
                left = left_list[i]
                right = left_list[i + 1]
                if content[left] == start_str and content[right] == end_str:
                    """
                    第一个字符串是开始，第二个字符串是结束
                    """
                    continue
                else:
                    if content[left] != start_str:
                        string_list = list(content)
                        string_list[left] = start_str
                        content = ''.join(string_list)
                    if content[right] != end_str:
                        string_list = list(content)
                        string_list[right] = end_str
                        content = ''.join(string_list)
        else:
            print('\n' + "-" * 100 + '')
            print("该章节(%s)的双引号异常，存在缺失或者错误位置，正在自动处理，若处理无效，请手动处理" % text_title_name)
            print("-" * 100)
            for i in range(len(left_list)):
                if len(left_list) == i + 2:
                    # 如果此时已经循环到最后一个了，
                    break
                if i % 2 != 0:
                    continue
                left = left_list[i]
                right = left_list[i + 1]
                if content[left] == start_str and content[right] == end_str:
                    """
                    第一个字符串是开始，第二个字符串是结束
                    """
                    continue
                else:
                    if content[left] != start_str:
                        string_list = list(content)
                        string_list[left] = start_str
                        content = ''.join(string_list)
                    if content[right] != end_str:
                        string_list = list(content)
                        string_list[right] = end_str
                        content = ''.join(string_list)
        return content

    def wrap_by_punctuation_mark(self, content: str) -> list:
        """
        按照标点符号进行换行
        :param content:
        :return:
        """
        change_line_str = template.wrap_character.value  # 句号之类的，如果碰到这个标点符号，就换行
        for i in change_line_str:
            if i != '':
                content_change = re.sub(i, i + '\n', content)
                content_list = content_change.split("\n")
                content = ""
                for n in range(len(content_list)):
                    if content_list[n][0:1] != "”":
                        content = content + '\n' + content_list[n]
                    else:
                        content = content + content_list[n]
        return content.split('\n')

    def wrap_by_punctuation_mark_line(self, content: str) -> list:
        """
        按照标点符号进行换行
        :param content:
        :return:
        """
        change_line_str = template.wrap_character_by_line.value  # 句号之类的，如果碰到这个标点符号，就换行
        for i in change_line_str:
            if i != '':
                content_change = re.sub(i, i + '\n', content)
                content_list = content_change.split("\n")
                content = ""
                for n in range(len(content_list)):
                    if content_list[n][0:1] != "”":
                        content = content + '\n' + content_list[n]
                    else:
                        content = content + content_list[n]
        return content.split('\n')

    def check_line_tips(self, content: str) -> bool:
        """
        检查这是否是完整的一句话
        :param content: 正文
        :return:
        """
        wrap_character = template.wrap_character_by_line.value
        if content.count("“") == content.count("”"):  # 有完整的开始双引号和结束双引号
            if content.count("“") > 0:
                start_str_index: list = [substr.start() for substr in re.finditer('“', content)]
                end_str_index: list = [substr.start() for substr in re.finditer('”', content)]
                for i in range(len(start_str_index)):
                    if int(start_str_index[i]) > int(end_str_index[i]):
                        """
                        如果出现了结束符的下标小于开始符，说明换行符异常
                        """
                        return False
                if any(wrap_str in content[-1:] for wrap_str in wrap_character):
                    """
                    如果结尾出现了表示可以结束的符号
                    """
                    return True
                else:
                    return False
            else:
                # 说明这里面没有双引号
                return True
        return False

    def line_feed_format(self, content_list: list or str) -> list:
        """
        对每一行的文本进行处理，检查双引号后面是否跟着不需要换行的字符, 单行模式使用
        :param content_list: 正文, 类型可以 list也可以传 str
        :return:
        """
        result_list = []
        content_list = [content_list] if type(content_list) == str else content_list
        for ii in range(len(content_list)):
            lines = content_list[ii]
            if lines.count("“") == lines.count("”"):  # 有完整的开始双引号和结束双引号。当然也可能没有，那就是  0 == 0
                if lines.count("“") > 0:
                    start_str_index: list = [substr.start() for substr in re.finditer('“', lines)]
                    end_str_index: list = [substr.start() for substr in re.finditer('”', lines)]

                    if "他肯定是感觉到了栗琳光滑的皮肤" in lines:
                        print("sss")
                    lines_temp: str = ""  # 用于存放换行后的字符
                    for i in range(len(start_str_index)):
                        # 开始检查
                        is_find = False
                        star_index = start_str_index[i + 1] if i < int(len(start_str_index) - 1) else -1
                        for end_str in template.end_str.value:
                            if lines[end_str_index[i]:star_index].find(end_str) == 1:
                                # 表示找到了，那么就不能换行
                                is_find = True

                        if lines[:1] == "“" and lines.count("“") == 1:
                            # 如果是以双引号开头的，并且这一行只有一组双引号，那么就在中间不换行了。应该这大概率是说话的词语在双引号之后。
                            lines_temp = lines + '\n'
                        elif is_find is False:
                            # 说明还是没找到
                            if i == 0:
                                # 说明是开始循环第一遍
                                lines_temp = lines_temp + lines[:end_str_index[i] + 1] + '\n' if star_index != -1 else lines_temp + lines[:end_str_index[i] + 1] + '\n' + lines[end_str_index[i] + 1:]
                            elif star_index == -1:
                                # 说明循环到了最后面
                                lines_temp = lines_temp + lines[end_str_index[i - 1] + 1:end_str_index[i] + 1] + '\n' + lines[end_str_index[i] + 1:]
                            else:
                                lines_temp = lines_temp + lines[end_str_index[i - 1] + 1:end_str_index[i] + 1] + '\n'
                        else:
                            # 说明找到了啊，那就不换行了
                            if i == 0:
                                # 说明是开始循环第一遍
                                lines_temp = lines_temp + lines[:end_str_index[
                                                                     i] + 1] if star_index != -1 else lines_temp + lines
                            elif star_index == -1:
                                # 说明循环到了最后面
                                lines_temp = lines_temp + lines[end_str_index[i - 1] + 1:end_str_index[i] + 1] + lines[end_str_index[i] + 1:]
                            else:
                                lines_temp = lines_temp + lines[end_str_index[i - 1] + 1:end_str_index[i] + 1]
                    if lines_temp != "":
                        for li in lines_temp.split('\n'):
                            if li != "":
                                result_list.append(li)
                    else:
                        result_list.append(lines)
                else:
                    # 说明没有双引号,那这句话就不要判断了
                    result_list.append(lines)
            else:
                result_list.append(lines)
        return result_list