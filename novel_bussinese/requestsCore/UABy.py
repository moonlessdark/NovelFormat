# 存放user_agent信息
from enum import Enum


class user_agent(Enum):
    android = "Mozilla/5.0 (Linux; Android 10; BMH-AN20 Build/HUAWEIBMH-AN20;) AppleWebKit/537.36 (KHTML, like Gecko) " \
              "Version/4.0 Chrome/88.0.4324.93 Mobile Safari/537.36 "

    ipad = "Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 " \
           "Mobile/9A334 Safari/7534.48.3 "

    ios = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) " \
          "Version/13.0.3 Mobile/15E148 Safari/604.1 "

    fireFox_windows = "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"

    fireFox_macos = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:92.0) Gecko/20100101 Firefox/92.0"

    chrome_windows = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53 "

    chrome_macos = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) " \
                   "Chrome/95.0.4638.69 Safari/537.36 "

    edge_windows = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                   "Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.53 "
