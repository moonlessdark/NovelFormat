from enum import Enum


class Template(Enum):
    # 网页垃圾字符
    error_str: list[str] = ["&amp;", "x5730;", "x5740;", "x53d1;", "x5e03;", "x9875;", "xff12;", "xff55;", "xff12;",
                            "xff55;", "xff12;", "xff55;", "xff0e;", "xff43;", "xff4f;", "xff4d;", "#x6700;", "#x65b0;",
                            "#x627e;", "#x56de;", "#xff14;", "#xff26;", "#xff14;", "#xff26;", "#xff14;", "#xff26;",
                            "#xff23;", "#xff2f;", "#xff2d;", "#x65B0;", "#x627E;", "#x56DE;", "#xFF14;", "#xFF26;",
                            "#xFF14;", "#xFF26;", "#xFF14;", "#xFF26;", "#xFF0E;", "#xFF23;", "#xFF2F;", "#xFF2D;",
                            "#x65B0;", "#x627E;", "#x56DE;", "#xFF14;", "#xFF26;", "#xFF14;", "#xFF26;", "#xFF14;",
                            "#xFF26;", "#xFF0E;", "#xFF23;", "#xFF2F;", "#xFF2D;"]

    """
    以下是换行判断
    """
    # 换行符，如果表示结束符的双引号右侧有该数组中的字符就换行，全局模式使用
    wrap_character: list[str] = ["。", "！", '；']

    # 结束符，碰到这些字符就开始检测是否需要换行，单行模式使用
    wrap_character_by_line: list = ["。", "？", "！", '；']

    # 表示说话的词语,用于判断是否需要换行。如果表示开始的双引号左侧有该数组中的字符，那么就在前面换行
    talk_str: list[str] = ['：', ':', '的说', '的道', "说道", "嘀咕", "笑骂", "怒骂", "骂道", "碎碎念", "大吼", "大叫", "笑道",
                           "嘟囔", "揶揄", "问道", '呵斥', '边唱', '边说', '边讲', '边问', '叮嘱', '吩咐', '唠叨', '调侃', '讨论',
                           '交流', '吩咐', '讲解', '七嘴八舌', '滔滔不绝', '口若悬河', '侃侃而谈', '念念有词', '振振有词', '喋喋不休',
                           '娓娓道来', '支支吾吾', '我说', '笑着说', '解释', '拍手说', '呻吟', '否认', '默念', '说']

    # 双引号右侧的第一个字符(例如：张三说："你说干啥子？", 李四闻言被吓了一大跳。)如果有以下字符，就不换行
    # 如果end_str和talk_str同时存在，那么优先判断end_str
    end_str: list[str] = ['。', '、', '了一声', '地一声', '的', '得一声', '的一下', '.', '，', '声', '一声闷哼', '问了声', '说着']

    # 小说中的推广广告，类似"记住最新网址XXXXXXXXXXX之类的"
    # 以下2个数组，用用于在正则表达式中，匹配符合"开头的字符+结尾的字符"的所有内容，将其置为Null
    # 英文括号 记得加上反斜杠转义一下
    ad_str: tuple[list[str, str]] = [('发布地址', '收藏不迷路！'),
                                     ('(天才只需一秒就能记住', 'com)'),
                                     ('最新找回', 'ＣＯＭ'),
                                     ('【最新发布地址', '找到回家的路!】'),
                                     ('【发布地址', 'COM】'),
                                     ('【天才一秒就记住', '以备不时之需！】'),
                                     ('【发布地址', '速记(看其他)】'),
                                     ('【记住收藏地址', '以备不时之需！】'),
                                     ('【发布地址', 'com】'),
                                     ('【最新地址发布页', '收藏不迷路!】'),
                                     ('【回家的路', '收藏不迷路!】'),
                                     ('【最新发布页', '收藏不迷路!】'),
                                     ('【收藏不迷路', '以备不时之需】'),
                                     ('地阯發鈽', '.com'),
                                     ('地阯发钚', '.com'),
                                     ('【手机看小说', '℃-〇-㎡】'),
                                     ('`w”w^w', 'n\'e”t^'),
                                     ('|最|新|网|址', '℃○㎡'),
                                     ('地~址~发~布~页~', 'C-0-M�')]
    # 词组，单词纠正
    change_str = [("。。", "。"),
                  ("壹", "一")]