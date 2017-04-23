# -*- coding: utf-8 -*-  

import datetime
import os
import re
import requests
import string
import thread
import time
import urllib2
import base64
import hashlib
from BeautifulSoup import BeautifulSoup
from INIFILE import INIFILE


# ----------- 加载处理糗事百科 -----------
class Spider_Model:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False
        self.canLoad = True #sub thread can run?
        self.store_dir = None
        self.init_work_dir()

        self.isFirst = True #run only once
        self.unload_page_num = 0 #page to be loaded
        # self.save_path = 'F:\\qiushimm\\'


    # init the storage dir = 'tmp /'
    def init_work_dir(self):
        retval = os.getcwd()
        print '#current dir is : ' + retval
        # 图片存放路径
        store_dir = retval + r'\tmp'
        print '#all imgs are going to be stored in dir :' + store_dir

        if not os.path.exists(store_dir):
            print '#tmp dir does not exist, attemp to mkdir'
            os.mkdir(store_dir)
            print '#mkdir sucessfully'
        else:
            print '#tmp dir is already exist'

        self.store_dir = store_dir

        # print '#now change current dir to tmp'
        # os.chdir(store_dir) #no neccessary
        # print os.getcwd()

    def print_commet(self):
        print '==================================='

    # 获取当前时间
    def now_date(self):
        # 获得当前时间
        now = datetime.datetime.now()  # ->这是时间数组格式
        # 转换为指定的格式:
        formateDate = now.strftime("%Y%m%d%H%M%S")
        return formateDate

    # 显示图片后缀名
    def file_extension(self, url):
        # get filename
        filename = os.path.basename(url)
        ext = os.path.splitext(filename)[1]
        return ext

    # 保存图片
    def saveFile(self, url, page, idx):
        user_define_name = self.now_date() + '_p_' + str(page) + '_' + string.zfill(idx, 2)  # 补齐2位
        file_ext = self.file_extension(url)  # 后缀名
        save_file_name = user_define_name + "_" + file_ext

        # 不能保存，改用open方法
        # urllib.urlretrieve(item[0], self.save_path + save_file_name)
        # 保存图片

        pic = requests.get(url)
        f = open(self.store_dir + '\\' + save_file_name, 'wb')
        f.write(pic.content)
        f.close()
        print '\ndone save file ' + save_file_name

    # 将所有的段子都扣出来，添加到列表中并且返回列表  
    def GetPage(self, page):
        site_url = base64.decodestring("aHR0cDovL3d3dy54aXVyci5jb20vcGFnZS8=")
        myUrl = site_url + page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(myUrl, headers=headers)

        print u'\n----background----now loading: page/' + page

        myResponse = urllib2.urlopen(req, data=None, timeout=10)
        myPage = myResponse.read()
        # encode的作用是将unicode编码转换成其他编码的字符串
        # decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("utf-8")
        # print type(unicodePage)

        #only do it once
        if self.isFirst:
            self.isFirst = False
            print '====================get the max page number===================='
            self.GetTotalPage(unicodePage)


        # if self.unload_page_num > int(page):
        #     print 'already done load all new page, stop thread now.'
        #     self.enable = False
        #     os._exit(0)

        # #re.S是任意匹配模式，也就是.可以匹配换行符
        # myItems[0]:the picurl; myItems[1]: the title
        #sometime, there are words between src & alt
        myItems = re.findall('<noscript><img.*? src="(.+?)".*?alt="(.*?)" /></noscript>', unicodePage, re.S)

        return myItems

    # get the max page number
    def GetTotalPage(self, html):
        # create the BeautifulSoup
        some_soup = BeautifulSoup(html)
        ele_a = some_soup.findAll('a', attrs={'class': 'page-numbers'})
        if len(ele_a) > 0:
            last_page_html = ele_a[len(ele_a) - 1]  # get the max page number.
            #print last_page_html

            # get the lastpage number
            pagenum = last_page_html.text

            self.SaveTotalPageToFile(pagenum)

    # store the max page number to totalpage.ini
    #new_page_num: new max page num
    def SaveTotalPageToFile(self, new_page_num):

        print '====================save the totalpage to totalpage.ini===================='

        file = INIFILE('totalpage.ini')

        # must write something if you set is_write to true. otherwise your file become empty.
        is_ok = file.Init(True, True)
        if not is_ok:
            print 'class initializing failed. check the [%s] file first.' % ('totalpage.ini')
            os._exit(0)

        old_page_num = file.GetValue('Main', 'totalpage')
        print '====================the old_page_num is [%s], the new_page_num is [%s]====================' % (old_page_num, new_page_num)
        file.SetValue('Main', 'totalpage', new_page_num)
        #close all
        file.UnInit()

        if int(new_page_num) >= int(old_page_num): #if there is new page
            self.unload_page_num = int(new_page_num) - int(old_page_num)
            if self.unload_page_num == 0:   #页码未增加，但是图片新增了
               self.unload_page_num = 1
            elif self.unload_page_num > 0: #增加新页面了，但是旧页上图片存在未下载的情况
                self.unload_page_num += 1
            print 'Ok, we got %s pages to load.' %(self.unload_page_num)
        else: #nothing new, stop main thread
            print 'Oops! Nothing new. exit main thread now.'
            os._exit(0) #terminal sub thread
            self.enable = False #terminal main thread

    # 用于加载新的段子  
    def LoadPage(self):
        # 如果用户未输入:q则一直运行  
        while self.canLoad:
            # 如果pages数组中的内容小于2个
            # print '\n----background----self.pages length: ' + str(len(self.pages))
            # 预加载2页数据
            if len(self.pages) < 2:
                try:
                    # 获取新的页面
                    myPage = self.GetPage(str(self.page))
                    self.page += 1
                    self.pages.append(myPage)
                    # print 'self.pages ' + str(len(self.pages))
                    # print '====================%s============%s' %(self.unload_page_num, self.page)
                    if self.unload_page_num < self.page:
                        print 'already load all new page, stop sub thread now.'
                        self.canLoad = False #let this thread do nothing

                except Exception, e:
                    # print '无法链接糗事百科！\n'
                    print e
            else:
                time.sleep(1)
                #print '\n----background----pause and wait.'
            #print '\n----background----sleep 2s, do not request too fast.'
            time.sleep(2)  # sleep 2s for test

    # show one page after press enter button.
    def ShowOnePage(self, now_page_items, page):
        for idx, item in enumerate(now_page_items):
            print "\ndownload " + item[1]
            self.saveFile(item[0], page, idx)
        print '========one page done.================='
        if self.unload_page_num == page:
            print '========all pages done. clean the repeated files.=========='
            self.CleanRepeatImage() #at last, deal with the repeated images.
            print 'Nothing left. Now close this application.'
            # self.enable = False  #let the main thread know it's time to quit
            os._exit(0) #can teminal main thread.

        # 输出一页后暂停
        myInput = raw_input()
        if myInput == ":q":
            self.enable = False

    # deal with the repeated image
    def CleanRepeatImage(self):
        if not os.path.exists('repeat'): #store the repeated file
            os.mkdir('repeat')

        hash_imgs = {}  # store the img_hash as key, the filepath as value..
        img_files = os.listdir('tmp')

        for file in img_files:
            # print type(file) the type of 'file' is str.
            f = open(os.path.join('tmp', file), 'rb')
            hash_img = hashlib.md5(f.read()).hexdigest()  # md5 this file.
            f.close()
            # print type(hash_img)
            # print hash_img
            if not hash_imgs.has_key(hash_img):
                hash_imgs[hash_img] = file
            else:
                print '--------------'
                print '%s already exsits.' % (file)  # the current file to be record.
                print hash_imgs.get(hash_img)  # the file already record.
                print '--------------'
                # keep the lastest "modified date" file
                f1 = os.path.join('tmp', file)
                f2 = os.path.join('tmp', hash_imgs.get(hash_img))
                f1_mtime = os.path.getmtime(f1)
                f2_mtime = os.path.getmtime(f2)
                if f1_mtime > f2_mtime:
                    # os.rename(f2, os.path.join('repeat', hash_imgs.get(hash_img)))
                    os.remove(f2) #or remove image
                else:
                    # os.rename(f1, os.path.join('repeat', file))
                    os.remove(f1) #or remove image

        print 'done delete repeat files.'


    def Start(self):
        self.enable = True
        page = self.page
        print u'正在加载中请稍候......'
        # 新建一个线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage, ())
        time.sleep(2) #wait the sub thread to be done.
        # ----------- 加载处理糗事百科 -----------
        while self.enable:
            # 如果self的page数组中存有元素
            if len(self.pages) > 0:
                now_page_items = self.pages[0]

                # del now page items
                del self.pages[0]

                self.ShowOnePage(now_page_items, page)
                page += 1

        print self.enable


# ----------- 程序的入口处 -----------
print u""" 
--------------------------------------- 
   程序：糗百爬虫 
   版本：0.3 
   作者：guzi
   日期：2016-12-29
   语言：Python 2.7 
   操作：输入:q退出
   功能：按下回车依次浏览
--------------------------------------- 
"""
myModel = Spider_Model()
print u'请按下回车浏览今日的糗百内容：'
raw_input(' ')
myModel.Start()
