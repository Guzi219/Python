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

import time
"""
对文件夹下的所有图片建立图片指纹（md5，hash），并以key，value方式录入数据库
"""
start_time = time.time()
# """
img_files = os.listdir('tmp')
img_files.sort() #默认名称排序
db = anydbm.open('md5.db','c')
for file in img_files:
    #print file
    f = open(os.path.join('tmp', file), 'rb')
    md5Str = hashlib.md5(f.read()).hexdigest()
    f.close()
    # print file + ": " + md5Str
    db[md5Str] = file
db.close()
# """
db = anydbm.open('md5.db','r')
print len(db.items())
for item in db.items():
    # print type(item)
    print item[0], ":" ,item[1]

end_time = time.time()
print 'costs %ds.' %(end_time  - start_time)