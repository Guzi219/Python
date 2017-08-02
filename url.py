# -*- coding: utf8 -*-
# url = "//ww1.sinaimg.cn/mw600/006HJ39wgy1ffo6mw2noaj30dw0ku0vp.jpg"
# print type(url)
# if not url.startswith('http') and url.startswith("//"):
#     url = "http:" + url
#     print url
#     print "success"
import anydbm
import os
import hashlib
img_files = os.listdir('tmp')
db = anydbm.open('md5.db','c')
for file in img_files:
    #print file
    f = open(os.path.join('tmp', file), 'rb')
    md5Str = hashlib.md5(f.read()).hexdigest()
    f.close()
    print file + ": " + md5Str
    db[md5Str] = file
db.close()


