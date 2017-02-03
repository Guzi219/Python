# -*- coding: utf8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup
import time
import re

class Tv_Dy2018:
    def __init__(self):
        self.base_url = 'http://www.dy2018.com'

    def LoadPage(self, myUrl):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        headers = {'User-Agent': user_agent, 'Accept': accept}
        print self.base_url + myUrl
        req = urllib2.Request(self.base_url+myUrl, headers=headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        #print myPage
        # encode的作用是将unicode编码转换成其他编码的字符串
        # decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("gb2312", 'ignore').encode('utf-8', 'ignore')
        # print unicodePage
        return unicodePage

    def ParseHtml(self, html):
        soup = BeautifulSoup(html)
        links = soup.findAll('a', attrs={'class': 'ulink'})
        #print len(links)
        if len(links) == 0: #the js return
            # tmp_js = soup.find(name='script', attrs={'language': 'javascript'})
            js_str = soup.script.string #two ways to get the <script></script>
            new_url = js_str[16:-1] #get the new url
            new_url = eval(new_url) #eval:计算字符串中的表达式
            self.ParseHtml(self.LoadPage(new_url))
        else:
            # print type(links)
            for link in links:
                # print type(link)
                # print type(link.string)
                print unicode(link.string)
                titles = re.findall(r'《(.+?)》', '2017年美国欧美剧《海豹六队第一季》连载至3') #unicode(link.string))
                print titles
                # print 'url is %s, title is %s.' %(link['href'], titles[0])

myUrl = '/html/tv/oumeitv/index.html'
myUrl2 = '/html/tv/oumeitv/index_2.html'
dy2018 = Tv_Dy2018()
dy2018.ParseHtml(dy2018.LoadPage(myUrl))
time.sleep(2) #rest 2s
dy2018.ParseHtml(dy2018.LoadPage(myUrl2))



