from requestsCore.requestBy import request as req


class getNovel:

    @staticmethod
    def get_novel(page_url, save_file_path):
        index_page_url = page_url  # 小说第一章第一页
        file_path = save_file_path  # 存放的文件夹
        next_page_url = None

        while True:
            if next_page_url is None:
                data = req().get(index_page_url)
            else:
                data = req().get("http://i.shubao12.cc/" + str(next_page_url))
            if data is not None:
                content = data.xpath("//div[@id='nr' and @class='nr_nr']/div[@id='nr1']/descendant-or-self::text()")
                next_page_name = data.xpath("//a[@id='pb_next']/descendant-or-self::text()")
                next_page_url_list = data.xpath("//a[@id='pb_next']/@href")
                title_name = data.xpath("//title/text()")

                title_name = title_name[0]

                if "下一页" or "下一章" in next_page_name:
                    if len(next_page_url_list) == 0:
                        break
                    next_page_url = next_page_url_list[0]
                    end_str = [".com", ".COM", ".C0M", "C〇M", ".net", "C0m", ".comc0M", ".comC0M", ".com:C0M", ':C0M']
                    for j in end_str:
                        if j in title_name:
                            title_name = title_name.replace(j, "")
                    file_name = file_path + title_name
                    file = open(file_name + ".txt", "a+", encoding="utf-8")
                    for i in content:
                        i = i.replace('\xa0', '')  # 去除空格
                        i = i.replace('“”', '')  # 去除这种里面没有内容的
                        if "本章未完" in i:  # 说明要翻页了，没必要存
                            continue
                        file.write(i)
                        file.write("\r\n")
                    file.close()
                else:
                    print("文章都下载下来了")
                    break
            else:
                print("小说下载失败，已终止")
                break
