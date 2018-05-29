# -*- coding: utf-8 -*-  

import datetime
import hashlib
import os
import string
import thread
import time
import urllib
import urllib2

import requests
from BeautifulSoup import BeautifulSoup
from INIFILE import INIFILE
from pip._vendor.requests import ReadTimeout
from requests.exceptions import MissingSchema
from selenium.webdriver.common.by import By

from Driver import Driver


# ----------- 加载处理糗事百科 -----------


class Spider_Model:
    def __init__(self):
        self.page = 1
        self.pages = []
        self.enable = False
        self.canLoad = True  # sub thread can run?
        self.allDone = False
        self.store_dir = None
        self.init_work_dir()

        self.isFirst = False  # run only once
        self.unload_page_num = 0  # page to be loaded

        # 主域名
        self.domainName = 'http://www.well1000.cn'
        # 模拟浏览器
        self.webDriverPage = Driver()
        # 第一个窗口
        self.windowOpenNum = 0
        # 从第二个开始关闭


    # init the storage dir = 'tmp /'
    def init_work_dir(self):
        retval = os.getcwd()
        print '#current dir is : ' + retval
        # 图片存放路径
        store_dir = retval + os.sep + 'tmp'
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
        url = self.CheckUrlValidate(url)
        try:
            pic = requests.get(url, timeout=10)
            f = open(self.store_dir + os.sep + save_file_name, 'wb')
            f.write(pic.content)
            f.close()
            print '\ndone save file ' + save_file_name
        except ReadTimeout:
            print 'save file %s failed. cause by timeout(10)' % (save_file_name)
        except MissingSchema:
            print 'invalid url %s' % (url)
        except Exception, e:
            print e

    # 保存文档
    def saveDocFile(self, doc, url, fileName):
        try:
            f = open(self.store_dir + os.sep + fileName, 'wb')
            f.write(doc.content)
            f.close()
            print '\ndone save file ' + fileName
        except ReadTimeout:
            print 'save file %s failed. cause by timeout(10)' % (fileName)
        except MissingSchema:
            print 'invalid url %s' % (url)
        except Exception, e:
            print e


    # 检查url是否包括http:协议
    def CheckUrlValidate(self, url):
        print url
        if not url.startswith('http') and url.startswith("//"):
            url = "http:" + url
        return url

    # 抓取单个页码中试题下载路径
    # 模拟浏览器打开
    def GetFileDownloadPath(self, pageUrl):
        pageUrl = self.domainName + pageUrl
        t0 = time.time()
        self.webDriverPage.start(pageUrl)
        t1 = time.time()
        print 'cost ' + (t1 - t0)
        # cookie
        cookies = self.webDriverPage.driver.get_cookies()

        #
        cookieStr = ''
        for cookie in cookies:
            # print cookie['name'], cookie['value']
            cookieStr = cookieStr + cookie['name'] + "=" + cookie['value'] + ";"
            # print type(cookie)
        cookieStr = cookieStr[:-1]

        link = self.webDriverPage.find_element(By.CSS_SELECTOR, 'div#biao a')
        fileDescTuple = ()
        fileDescTuple = (link.get_attribute('href'), link.text)
        self.downloadFile(fileDescTuple, pageUrl, cookieStr)


    # 下载文件主程序
    def downloadFile(self, fileDescTuple, referUrl, cookieStr):
        if len(fileDescTuple) == 2 :
            fileLink = fileDescTuple[0]
            fileDesc = fileDescTuple[1]

            # 网站验证rerfer是否属于本网站，并且验证cookie{title,id}是否存在，不验证值

            myHeaders = {
                'Referer': referUrl,
                'Cookie': cookieStr
            }
            doc = requests.get(fileLink, headers = myHeaders, timeout=10)
            # print urllib.parse.unquote(r.headers['Content-Disposition'])
            # print r.headers['Content-Disposition']
            # print type(r.headers['Content-Disposition'])
            #urldecode
            fileName =  urllib.unquote(doc.headers['Content-Disposition'])
            fileName = fileName[len('attachment; filename='):]
            print 'download : ' + fileName
            fileName = unicode(fileName, "utf-8")
            print type(fileName)
            self.saveDocFile(doc, fileLink, fileName)
            if not self.isFirstWindow:
                self.webDriverPage.close()
                self.isFirstWindow = False


    # 将所有的段子都扣出来，添加到列表中并且返回列表
    def GetPage(self, page):
        site_url = 'http://www.well1000.cn/so/search_well.aspx?wd=%E4%B9%9D%E5%B9%B4%E7%BA%A7%20%E4%B8%AD%E8%80%83%202018%20%E8%8B%B1%E8%AF%AD'
        myUrl = site_url + '&pg=' + page
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(myUrl, headers=headers)

        print u'\n----background----now loading: page/' + page

        myResponse = urllib2.urlopen(req, data=None, timeout=10)

        # 检测网页编码
        # print chardet.detect(myResponse.read())

        # 将获取的字符串strTxt做decode时，指明ignore，会忽略非gb2312编码的字符
        myPage = myResponse.read()
        # .decode('gb2312','ignore').encode('utf-8')
        # encode的作用是将unicode编码转换成其他编码的字符串
        # decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("utf-8")

        # remove emoji[when this page get emoji inside, it'll run error:unichr() arg not in range(0x10000) (narrow Python build)]
        # unicodePage= emojiutil.remove_define_emoji(unicodePage)

        # only do it once
        if self.isFirst:
            self.isFirst = False
            print '====================get the max page number===================='
            self.GetTotalPage(unicodePage)

        # if self.unload_page_num > int(page):
        #     print 'already done load all new page, stop thread now.'
        #     self.enable = False
        #     os._exit(0)

        link_soups = BeautifulSoup(unicodePage)
        # print(link_soups)
        # 格式如下（每页20个）
        # <a href="/stdown/yingyu/122541.html" target="_blank"><font color="#FF0000">2018</font>年<font color="#FF0000">中考</font><font color="#FF0000">英语</font>一轮教材复习精练(<font color="#FF0000">九年级</font>上module11～12)有答案</a>
        articleUrls = link_soups.findAll('a', attrs={'target': '_blank'})
        myItems = []  # list: store the tup(src, alt)
        for oneArticleUrl in articleUrls:
            try:
                tup1 = (oneArticleUrl['href'], oneArticleUrl.text)
                myItems.append(tup1)
            except KeyError, e:  # if u can't get key attr
                print 'KeyError', e
            except Exception, e:
                print 'Other Error', e

        return myItems


    # get the max page number
    def GetTotalPage(self, html):
        # create the BeautifulSoup
        some_soup = BeautifulSoup(html)
        # get the page div
        ele_a = some_soup.find('td', attrs={'class': 'linear'})
        # get the last div>a text='末页'
        last_a = ele_a.findAll('em')[-1]
        # get total num
        total_num = ele_a.findAll('em')[1]
        print ('共计查询结果：' + total_num.text.encode('utf-8'))
        # substr 0:.html
        pagenum = last_a.text  # .get('href')[:-5]
        print ('共计页码 : ' + pagenum.encode('utf-8'))
        # print type(last_a)

        self.SaveTotalPageToFile(pagenum)

        # store the max page number to totalpage.ini


    # new_page_num: new max page num
    def SaveTotalPageToFile(self, new_page_num):
        print '====================save the totalpage to totalpage.ini===================='

        proFileName = 'english_download.ini'
        file = INIFILE(proFileName)

        # must write something if you set is_write to true. otherwise your file become empty.
        is_ok = file.Init(True, True)
        if not is_ok:
            print 'class initializing failed. check the [%s] file first.' % (proFileName)
            os._exit(0)

        old_page_num = file.GetValue('Main', 'totalpage')
        print '====================the old_page_num is [%s], the new_page_num is [%s]====================' % (
            old_page_num, new_page_num)
        file.SetValue('Main', 'totalpage', new_page_num)
        # close all
        file.UnInit()

        if int(new_page_num) >= int(old_page_num):  # if there is new page
            # self.unload_page_num = int(new_page_num) - int(old_page_num)
            self.unload_page_num = int(new_page_num) - int(old_page_num)
            if self.unload_page_num == 0:  # 页码未增加，但是图片新增了
                self.unload_page_num = 1
            elif self.unload_page_num > 0:  # 增加新页面了，但是旧页上图片存在未下载的情况***会导致下载不会结束
                self.unload_page_num += 1
            print 'since we start at page %s, we still got (%s-%s) pages to load.' % (
                self.page, self.unload_page_num, self.page)
        else:  # nothing new, stop main thread
            print 'Oops! Nothing new. exit main thread now.'
            os._exit(0)  # terminal sub thread
            self.enable = False  # terminal main thread


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
                    print '====================%s============%s' % (self.unload_page_num, self.page)
                    if self.unload_page_num <= self.page:
                        print 'already load all new page, stop sub thread now.'
                        self.canLoad = False  # let this thread do nothing
                        self.allDone = True

                except Exception, e:
                    print e
            else:
                time.sleep(1)
                # print '\n----background----pause and wait.'
            # print '\n----background----sleep 2s, do not request too fast.'
            time.sleep(2)  # sleep 2s for test


    # show one page after press enter button.
    def ShowOnePage(self, now_page_items, page):
        for idx, item in enumerate(now_page_items):
            print "\nopen " + item[0]
            self.GetFileDownloadPath(item[0])
        # print '========one page done.================='
        print '========Please hit the Enter.================='
        # if self.unload_page_num == page:
        if self.allDone:
            # print '========all pages done. clean the repeated files.=========='
            # self.CleanRepeatImage() #at last, deal with the repeated images.
            print 'Nothing left. Now close this application.'
            # self.enable = False  #let the main thread know it's time to quit
            os._exit(0)  # can teminal main thread.

        # 输出一页后暂停
        time.sleep(1)
        print 'take a snap for 1s.'
        # 手动抓取
        myInput = raw_input()
        # if myInput == ":q":
        #     self.CleanRepeatImage() #if break manually, must clean work dir.
        #     self.enable = False


    # deal with the repeated image
    def CleanRepeatImage(self):
        if not os.path.exists('repeat'):  # store the repeated file
            os.mkdir('repeat')

        hash_imgs = {}  # store the img_hash as key, the filepath as value..
        img_files = os.listdir('tmp')
        img_files.sort()
        for file in img_files:
            # print file
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
                # remove it
                f1 = os.path.join('tmp', file)
                os.remove(f1)

        print 'done delete repeat files.'


    def Start(self):
        self.enable = True
        page = self.page
        print u'正在加载中请稍候......'
        # 新建一个线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage, ())
        time.sleep(2)  # wait the sub thread to be done.
        # ----------- 加载处理糗事百科 -----------
        while self.enable:
            # 如果self的page数组中存有元素
            if len(self.pages) > 0:
                now_page_items = self.pages[0]

                # del now page items
                del self.pages[0]
                print '---main thred --', page
                self.ShowOnePage(now_page_items, page)
                page += 1

        print self.enable  # ----------- 程序的入口处 -----------


print u"""
--------------------------------------- 
   程序：英语网站--爬虫
   版本：2.7
   作者：guzi
   日期：2018年5月26日
   语言：Python 2.7 
   操作：输入:q退出
   功能：按下回车依次浏览
--------------------------------------- 
"""
myModel = Spider_Model()
print u'请按下回车浏览英语下载网站：'
raw_input(' ')
# myModel.page=913 #start from which page, default 1
myModel.Start()
# myModel.CleanRepeatImage()
