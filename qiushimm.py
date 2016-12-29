# -*- coding: utf-8 -*-  

import datetime
import os
import re
import requests
import string
import thread
import time
import urllib2


#----------- 加载处理糗事百科 -----------
class Spider_Model:  
      
    def __init__(self):  
        self.page = 1
        self.pages = []  
        self.enable = False
        self.save_path = 'F:\\qiushimm\\'

    #获取当前时间
    def now_date(self):
        # 获得当前时间
        now = datetime.datetime.now()  # ->这是时间数组格式
        # 转换为指定的格式:
        formateDate = now.strftime("%Y%m%d")
        return formateDate

    #显示图片后缀名
    def file_extension(self, url):
        #get filename
        filename = os.path.basename(url)
        ext = os.path.splitext(filename)[1]
        return ext

    #保存图片
    def saveFile(self, url, page, idx):
        user_define_name = self.now_date() + '_p_' + str(page) + '_' + string.zfill(idx, 2)  # 补齐2位
        file_ext = self.file_extension(url)     #后缀名
        save_file_name = user_define_name + "_" + file_ext

        # 不能保存，改用open方法
        # urllib.urlretrieve(item[0], self.save_path + save_file_name)
        # 保存图片

        pic = requests.get(url)
        f = open(save_file_name, 'wb')
        f.write(pic.content)
        f.close()
        print '\ndone save file ' + save_file_name

    # 将所有的段子都扣出来，添加到列表中并且返回列表  
    def GetPage(self,page):  
        myUrl = "http://www.qiushimm.com/page/" + page  
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' 
        headers = { 'User-Agent' : user_agent } 
        req = urllib2.Request(myUrl, headers = headers)

        print u'\n----background----now loading: ' + myUrl
        
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()  
        #encode的作用是将unicode编码转换成其他编码的字符串  
        #decode的作用是将其他编码的字符串转换成unicode编码  
        unicodePage = myPage.decode("utf-8")

        #re.S是任意匹配模式，也就是.可以匹配换行符
        myItems = re.findall('<noscript><img.*? src="(.+?)" alt="(.*?)" /></noscript>',unicodePage,re.S)

        return myItems  
  
    # 用于加载新的段子  
    def LoadPage(self):  
        # 如果用户未输入quit则一直运行  
        while self.enable:  
            # 如果pages数组中的内容小于2个
            print '\n----background----self.pages length: ' + str(len(self.pages))
            #预加载2页数据
            if len(self.pages) < 2:
                try:  
                    # 获取新的页面
                    myPage = self.GetPage(str(self.page))
                    self.page += 1  
                    self.pages.append(myPage)  
                except Exception,e:  
                    #print '无法链接糗事百科！\n'
                    print e
            else:  
                time.sleep(1)
                print '\n----background----pause and wait.'
            print '\n----background----sleep 2s, do not request too fast.'
            time.sleep(2)  # sleep 2s for test
          
    def ShowOnePage(self,now_page_items,page):
        for idx, item in enumerate(now_page_items):
            print "\ndownload " + item[1]
            self.saveFile(item[0], page, idx)


        #输出一页后暂停
        myInput = raw_input()
        if myInput == ":q":
            self.enable = False

            
    def Start(self):
        self.enable = True
        page = self.page
        print u'正在加载中请稍候......'
        # 新建一个线程在后台加载段子并存储
        thread.start_new_thread(self.LoadPage,())
        #----------- 加载处理糗事百科 -----------
        while self.enable:
            # 如果self的page数组中存有元素
            if self.pages:
                now_page_items = self.pages[0]
                #del now page items
                del self.pages[0]

                self.ShowOnePage(now_page_items,page)
                page += 1
  
  
#----------- 程序的入口处 -----------  
print u""" 
--------------------------------------- 
   程序：糗百爬虫 
   版本：0.3 
   作者：why 
   日期：2016-12-29
   语言：Python 2.7 
   操作：输入quit退出阅读糗事百科 
   功能：按下回车依次浏览今日的糗百热点 
--------------------------------------- 
"""
  
  
print u'请按下回车浏览今日的糗百内容：'
# 查看当前工作目录
retval = os.getcwd()
print "当前工作目录为 %s" % retval

# 修改当前工作目录
os.chdir('F:\\qiushimm\\')

# 查看修改后的工作目录
retval = os.getcwd()

print "目录修改成功 %s" % retval


raw_input(' ')  
myModel = Spider_Model()  
myModel.Start()  
