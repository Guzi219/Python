# -*- coding: utf8 -*-
# import base64
# =====base64 encode, decode
# s1 = base64.encodestring('http://www.qiushimm.com/page/')
# s2 = base64.decodestring(s1)
# print s1,s2
from BeautifulSoup import BeautifulSoup
from INIFILE import INIFILE
import random

soup = BeautifulSoup('<em title="python" class="boldest ts" value="hh">Extremely bold</em>')
tag = soup.em
print type(tag)
print tag.name
print tag.attrs
print '####value'
print tag.get('value')

tag['class'] = 'verybold'
tag['id'] = 1
print tag

print soup

# nouse don't know why
# tag = soup.find(class_='verybold')

tag = soup.find(attrs={'class': 'verybold'})
if tag:
    print tag.get('title')
    print tag['id']

some_html = '''
<div class="pagination clearfix">
			<div class="yuguo-pagenavi"><span class="page-numbers current">1</span>
<a class="page-numbers" href="http://www.qiushimm.com/page/2">2</a>
<a class="page-numbers" href="http://www.qiushimm.com/page/3">3</a>
<span class="page-numbers dots">…</span>
<a class="page-numbers" href="http://www.qiushimm.com/page/802">802</a>
<a class="next page-numbers" href="http://www.qiushimm.com/page/2">下一页»</a></div>
			</div>
'''
# print some_html

# some_soup = BeautifulSoup(some_html)
# ele_a = some_soup.findAll('a', attrs={'class': 'page-numbers'})
# if len(ele_a) > 0:
#     last_page_html = ele_a[len(ele_a) - 1]
#     print last_page_html
#     print type(last_page_html)
#     # get the lastpage number
#     print last_page_html.text

print '============================'
file = INIFILE('totalpage.ini')

#must write something if you set is_write to true. otherwise your file become empty.
is_ok = file.Init(True, True)
if not is_ok:
    print 'class initializing failed. check the [%s] file first.' % ('totalpage.ini')
    exit(0)
num = file.GetValue('Main', 'totalpage')
print 'the toalpage is [%s]' % (num)
file.SetValue('Main', 'totalpage', 800)

# print file.GetValue('Main', 'TotalPage', '0')

# file.SetValue('DEMO', 'whoami', 'Admin')
# print file.GetValue('DEMO', 'whoami', 'Admin')

file.UnInit()
