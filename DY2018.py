# -*- coding: utf8 -*-
import urllib2
from BeautifulSoup import BeautifulSoup

myUrl = 'http://www.dy2018.com/html/tv/oumeitv/index.html'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
headers = {'User-Agent': user_agent, 'Accept': accept}
req = urllib2.Request(myUrl, headers=headers)

myResponse = urllib2.urlopen(req)
myPage = myResponse.read()
#print myPage
# encode的作用是将unicode编码转换成其他编码的字符串
# decode的作用是将其他编码的字符串转换成unicode编码
unicodePage = myPage.decode("gb2312", 'ignore').encode('utf-8', 'ignore')

print unicodePage
soup = BeautifulSoup(unicodePage)

links = soup.findAll('a', attrs={'class': 'ulink'})
# print type(links)
for link in links:
    print link