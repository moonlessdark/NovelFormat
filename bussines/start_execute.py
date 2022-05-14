from Tools.formatText.formatContent import formatByRule


class executeFormat():

    """
    开始执行
    """

    def __init__(self):
        self.f = formatByRule()

    # def star_format(self, content_list: list) -> list:
    #     """
    #     组装在一起执行
    #     :param content_list:
    #     :return:
    #     """
    #     format_content_list = []
    #     if len(content_list) > 0:
    #         for i in content_list:
    #             if i != "":
    #                 step_1_list = self.f.in_the_middle_of_two_sentences(i)
    #                 for y in step_1_list:
    #                     step_2_list = self.f.format_end_str(y)
    #                     for k in step_2_list:
    #                         step_3_list = self.f.format_start_str(k)
    #                         for j in step_3_list:
    #                             format_content_list.append(j)
    #         return format_content_list
    #     else:
    #         return content_list

    def star_format(self, content_list: list) -> list:
        """
        组装在一起执行
        :param content_list:
        :return:
        """
        format_content_list = []
        if len(content_list) > 0:
            for i in content_list:
                if i != "":
                    step_2_list = self.f.wrap_by_punctuation_mark(i)  # 先统一按标点符号进行换行
                    for j in step_2_list:
                        format_content_list.append(j)
            list_2 = self.f.merge_talk(format_content_list)  # 把所有双引号中间的文案都合并到同一行，个人习惯问题
            list_3 = self.f.wrap_by_str(list_2)  # 再次判断一下双引号左右2边的文案有没有说话的动词，再来判断是不是要换行。这是因为双引号里的内容并不一定代表了说话，也可能是表示重点信息
            return list_3
        else:
            return content_list
