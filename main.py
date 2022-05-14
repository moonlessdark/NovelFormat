from datetime import datetime
from multiprocessing import Pool
from Tools.textToPackage import *
from Tools.getPageText.getPage import *
from Tools.fileOpt import *
from Tools.formatText.formatContent import formatByRule
from bussines.start_execute import executeFormat


def get_novel(page_url, save_file_path):
    """
    通过url下载小说
    :param page_url:
    :param save_file_path:
    :return:
    """
    getNovel.get_novel(page_url, save_file_path)


def format_content_2(origin_text_path: str, save_format_text_path: str, text_name: str):
    """

    :param origin_text_path: 待处理的txt文件path
    :param save_format_text_path: 存储格式化后的文件夹路径
    :param text_name: 存储的文件名
    :return:
    """
    ys = fileOpt.read_file(origin_text_path)  # 读取文件
    ys = formatContent().clear_wrap_text(ys)  # 清理所有的换行符
    ys = formatByRule().format_end_2_start_double_quotation_mark(ys)  # 先拆分2个对话之间的数据
    ys = executeFormat().star_format(ys)
    fileOpt.save_txt(ys, save_format_text_path, text_name)


if __name__ == "__main__":
    save_folder_path = "D:/Download/新建文件夹/test/"  # 下载txt文件存储的地址
    save_format_text_path = "D:/Download/新建文件夹/format/"  # 格式化下载的文件存储的地址

    # get_novel(page_url="http://i.shubao12.cc/2_2777/60691.html", save_file_path=save_folder_path)  # 下载小说，从第一章第一页开始

    # 下载完了，开始格式化小说
    file_list = fileOpt.read_file_path(save_folder_path)
    po = Pool(5)
    print("开始执行")
    for i in range(len(file_list)):
        file_path = save_folder_path + str(file_list[i])
        print(datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')+"==>开始处理：" + str(file_list[i]))
        po.apply_async(format_content_2(origin_text_path=file_path, save_format_text_path=save_format_text_path, text_name=str(file_list[i])), (i,))
    po.close()
    po.join()
    print("结束了")
