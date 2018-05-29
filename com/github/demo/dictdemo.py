# -*- coding: utf-8 -*-
from urllib import unquote, urlencode

# string = 'attachment; filename=%e5%8d%83%e6%95%99%e7%bd%91%ef%bc%8d2018%e5%b9%b4%e4%b8%ad%e8%80%83%e8%8b%b1%e8%af%ad%e4%b8%80%e8%bd%ae%e6%95%99%e6%9d%90%e5%a4%8d%e4%b9%a0%e7%b2%be%e7%bb%83(%e4%b9%9d%e5%b9%b4%e7%ba%a7%e4%b8%8amodule1%ef%bd%9e2)%e6%9c%89%e7%ad%94%e6%a1%88AwUAlK.doc'
# fileName =  unquote(string)
# print fileName
# print fileName.index('attachment; filename=')
# print fileName[len('attachment; filename='):]
#
# string2 = 'http://www.well1000.cn/so/search_well.aspx?wd=%E4%B9%9D%E5%B9%B4%E7%BA%A7%20%E4%B8%AD%E8%80%83%202018%20%E8%8B%B1%E8%AF%AD'
#
# wd='http://www.well1000.cn/so/search_well.aspx?wd=九年级 中考 2018 英语'
# data = {'wd':'九年级 中考 2018 英语'}
# print urlencode(data)
# print unquote(urlencode(data))


filterWords = ['中考', '英语']
path = ['千教网－江西省赣州市十四县(市)2017-2018学年高二下学期期中联考英语试卷word版有答案中考AKHHwn', '英语期中考试题', '千教网－2017-2018学年泽林牛津版八年级下英语期中试卷含听力mp3AKHHKM']
for p in path:
    flag = True
    for word in filterWords:
        # print word
        if p.find(word) == -1:
            flag = False
            break
    if flag:
        print p