import os

import chardet

from Tools.tradition import tradition2simple


class fileOpt:

    @staticmethod
    def read_file_path(folder_path: str):
        """

        :param folder_path: txt存放的文件夹
        :return:
        """
        file_list = os.listdir(folder_path)
        file_list.sort(key=lambda fn: os.path.getmtime(folder_path + '/' + fn))
        return file_list

    @staticmethod
    def read_file(file_path) -> str:
        """
        读取单文件
        :param file_path: txt文件的路径
        :return:
        """
        error_str = ["&amp;", "x5730;", "x5740;", "x53d1;", "x5e03;", "x9875;", "xff12;", "xff55;", "xff12;", "xff55;",
                     "xff12;", "xff55;", "xff0e;", "xff43;", "xff4f;", "xff4d;", "#x6700;", "#x65b0;", "#x627e;",
                     "#x56de;", "#xff14;", "#xff26;", "#xff14;", "#xff26;", "#xff14;", "#xff26;", "#xff23;", "#xff2f;",
                     "#xff2d;", "#x65B0;", "#x627E;", "#x56DE;", "#xFF14;", "#xFF26;", "#xFF14;", "#xFF26;", "#xFF14;",
                     "#xFF26;", "#xFF0E;", "#xFF23;", "#xFF2F;", "#xFF2D;", "#x65B0;", "#x627E;", "#x56DE;",
                     "#xFF14;", "#xFF26;", "#xFF14;", "#xFF26;", "#xFF14;", "#xFF26;", "#xFF0E;", "#xFF23;", "#xFF2F;",
                     "#xFF2D;"]
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


