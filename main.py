import time
from multiprocessing import Pool
from Tools.textToPackage import *
from Tools.fileOpt import *
from bussines.action_execute.start_execute import executeFormat
from bussines.format_mode.common import format_common
from bussines.format_mode.global_mode import formatByGlobal2
from bussines.format_mode.sigle_line_mode import formatByLine
from bussines.get_page_content.get_by_shubao12.getPage import getNovel


def get_novel(page_url, save_file_path):
    """
    通过url下载小说
    :param page_url: 第一章第一页的url
    :param save_file_path: 下载的内容的保存路径
    :return:
    """
    getNovel.get_novel(page_url, save_file_path)


def format_content_global_mode(origin_text_path: str, format_text_save_path: str, text_name: str):
    """
    全局检测模式，按照规则重新换行
    :param origin_text_path: 待处理的txt文件path
    :param format_text_save_path: 存储格式化后的文件夹路径
    :param text_name: 存储的文件名
    :return:
    """
    ys = fileOpt.read_file(origin_text_path)  # 读取文件
    ys = formatContent().clear_wrap_text(ys)  # 清理所有的换行符
    ys = format_common().format_end_2_start_double_quotation_mark(content=ys, text_title_name=text_name)  # 先拆分2个对话之间的数据
    ys = executeFormat().star_format_global_mode(ys)
    fileOpt.save_txt(ys, format_text_save_path, text_name)


def format_content_global_mode_2(origin_text_path: str, format_text_save_path: str, text_name: str):
    """
    全局检测模式，按照规则重新换行
    :param origin_text_path: 待处理的txt文件path
    :param format_text_save_path: 存储格式化后的文件夹路径
    :param text_name: 存储的文件名
    :return:
    """
    ys = fileOpt.read_file(origin_text_path)  # 读取文件
    # clear_ad_content: str = format_common().clear_ad_str(ys)
    ys = format_common().format_end_2_start_double_quotation_mark(content=ys, text_title_name=text_name)  # 先拆分2个对话之间的数据
    r_result = formatByGlobal2().line_feed_by_str(ys)
    re_list = formatByGlobal2().format_end_str(r_result)
    s = format_common().line_feed_format(re_list)
    fileOpt.save_txt(s, format_text_save_path, text_name)


def format_content_line_mode(origin_text_path: str, format_text_save_path: str, text_name: str):
    """
    单行检测模式，只真对每一行来判断是否需要换行。如果作者本身就没有良好的换行习惯的话，会变得很长。
    :param origin_text_path: 待处理的txt文件path
    :param format_text_save_path: 存储格式化后的文件夹路径
    :param text_name: 存储的文件名
    :return:
    """
    ys = fileOpt.read_file(origin_text_path)  # 读取文件
    r_list = formatByLine().split_by_line_feed(content=ys, text_title_name=text_name)  # 清理换行符
    r_result = executeFormat().star_format_line_mode(r_list)
    fileOpt.save_txt(r_result, format_text_save_path, text_name)


if __name__ == "__main__":
    save_folder_path = "D:/Download/新建文件夹/test/"  # 下载txt文件存储的地址
    save_format_text_path = "D:/Download/新建文件夹/format/"  # 格式化下载的文件存储的地址

    # get_novel(page_url="http://i.shubao12.cc/3_3469/64419.html", save_file_path=save_folder_path)  # 下载小说，从第一章第一页开始

    # 下载完了，开始格式化小说
    file_list = fileOpt.read_file_path(save_folder_path)
    po = Pool(5)
    print("开始执行")
    for i in range(len(file_list)):
        file_path = save_folder_path + str(file_list[i])
        # 根据自己的需求替换全局模式的方法还是单行模式的方法
        po.apply_async(format_content_line_mode(origin_text_path=file_path, format_text_save_path=save_format_text_path, text_name=str(file_list[i])), (i,))
        print('\n', end='')
        print("已处理： {}%  ".format(round((i+1)/len(file_list)*100, 2)), end="", flush=True)
        time.sleep(0.5)
    po.close()
    po.join()
    print('\n', end='')
    print("结束了")
