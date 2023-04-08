import os

import chardet

from novel_bussinese.Tools.tradition import tradition2simple
from novel_bussinese.template.rexp_template import Template


class FileOpt:
    """
    文件操作
    """

    @staticmethod
    def read_file_path(folder_path: str):
        """
        获取文件路径
        :param folder_path: txt存放的文件夹
        :return:
        """
        file_list = os.listdir(folder_path)
        file_list.sort(key=lambda fn: os.path.getmtime(folder_path + '/' + fn))
        return file_list

    @staticmethod
    def read_file(file_path) -> str:
        """
        读取text文件，进行字体转换，并清除一些垃圾字符
        :param file_path: txt文件的路径
        :return:
        """
        error_str = Template.error_str.value
        with open(file_path, "rb") as f:
            content = f.read()
        content_encode = chardet.detect(content)  # 推断一下文本内容的编码格式
        if "gb" in content_encode.get("encoding"):
            with open(file_path, encoding="gb18030") as file:
                read_content = file.read()
        elif "Windows-1252" in content_encode.get("encoding"):
            read_content = content.decode("windows-1252")
        else:
            with open(file_path, encoding="utf-8") as file:
                read_content = file.read()
        read_content = tradition2simple(read_content)
        for i in error_str:
            """
            处理一下垃圾字符串
            """
            if i in read_content:
                read_content = read_content.replace(i, "")
        return read_content

    @staticmethod
    def save_txt(content, text_path: str, text_name: str):
        text_path = text_path + '/' if '/' != text_path[-1:] else text_path
        text_name = str(text_name)
        text_name = text_name + ".txt" if ".txt" not in text_name else text_name
        if len(content) > 0:
            if type(content) == list:
                content_str = ""
                for i in range(len(content)):
                    if content[i] != "":
                        content_str = content_str + content[i] + "\r\n"
                with open(text_path + text_name, "w+", encoding="utf-8") as f:
                    f.write(content_str)
            else:
                with open(text_path + text_name, "w+", encoding="utf-8") as f:
                    f.write(content)

    @staticmethod
    def tradition2simple(content: str):
        """
        繁转简
        :param content:
        :return:
        """
        return tradition2simple(content)
