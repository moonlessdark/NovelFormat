import zhconv


def tradition2simple(hans_str: str):
    '''
    Function: 将 hans_str 由简体转化为繁体
    '''
    return zhconv.convert(hans_str, 'zh-cn')