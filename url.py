# -*- coding: utf8 -*-
url = "//ww1.sinaimg.cn/mw600/006HJ39wgy1ffo6mw2noaj30dw0ku0vp.jpg"
print type(url)
if not url.startswith('http') and url.startswith("//"):
    url = "http:" + url
    print url
    print "success"


