# -*- coding:utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

OVER_TIME = 2
# BASE_URL = "https://www.dy2018.com/html/gndy/dyzz/index.html"
BASE_URL = "http://sj.zxxk.com/"
# MAIN_PAGE1 = "http://sj.zxxk.com/sj/yy-type1-g9/2018/?pagesize=10&uk=中考"
MAIN_PAGE1 = "http://sj.zxxk.com/sj/yy-type1-g7/2018/?pagesize=10&uk=中考"


class Driver(object):
    u"""
    需要登陆，有账号登陆ip限制
    """
    def __init__(self, driver_name="Chrome"):
        print 'DriverSingleton __init__'
        if driver_name == "Firefox":
            self.driver = webdriver.Firefox()
        elif driver_name == "Ie":
            self.driver = webdriver.Ie()
        else:
            # 不打开浏览器窗口
            # chrome_options = Options()
            # chrome_options.add_argument('--headless')
            # chrome_options.add_argument('--disable-gpu')
            # self.driver = webdriver.Chrome(chrome_options=chrome_options)

            options = webdriver.ChromeOptions()
            prefs = {
                'profile.default_content_setting_values': {
                    'images': 2
                    # ,
                    # 'javascript': 2
                },
                'profile.default_content_settings.popups': 0,
                'download.default_directory': 'F:\\个人\\学科网'
            }
            # options.add_experimental_option('prefs', prefs)
            self.driver = webdriver.Chrome(chrome_options=options)

        self.driver.implicitly_wait(OVER_TIME)

    def __new__(cls, *args, **kw):
        """
        使用单例模式将类设置为运行时只有一个实例，在其他Python类中使用基类时，
        可以创建多个对象，保证所有的对象都是基于一个浏览器
        """
        if not hasattr(cls, '_instance'):
            orig = super(Driver, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
            print('run only once.')
        return cls._instance

    def start(self, url=BASE_URL):
        """
        启动浏览器
        :param url: 测试地址
        :return:
        """
        self.driver.get(url)
        # 添加登陆cookie
        self.driver.add_cookie({'name': 'xk.passport', 'value': 'ED6EEBFEFDDE7CD6BF19065C8D8C2EC6C8192DDF5F136FB3300F92221D478B12DAC27EFB746BDE1994282365F8192FA99100EEF8E0A8EA3ED683D4BED4B9627E0D7C338A8A75EEF95A06F9D473299A2838D41BB0FEDCD868EBBCDBDB14459A24C7383764CC4BDB9370B3151B4EF5B66032F0A27171FDE997B4BD2BB855767A17EA511CD2A15C522E253C3228EF4836A765D49AC3607E10201F08A804FBEC97E1D0B73BC42F69FD40FA26D9ADAA8558725DEC8D08958F6BEF900440B614240F2E5A29972DEAE89C45DE6B1DBAD9306A9A7833470C326A6359FD3E0889EE3D37AE1854B5974011F2B02E8F1087FD11B9A079B0759D896876D8A77115AF0620781ED025835373AFF76FA6B9C49B7310720C4DDD5D72C82F3C697124D158E46884ADBCC8956D703AF45E054EE25502CC39644E6D6D6EFD078E71FC7D911C33B5FB47AB9FA3507F8147417E016688084DDC59903C67DF2D38CE69971F3EDB11485AC344F0DE70363B0DA5CA025D3912825782F12E59DAA0581E1AFFF2BA1B457CD88943F57EC34160F35C9F5768B80342606349E5A83B676ACD542918A8BC77083AA3BA17F6F81B155332B94DD311A7DA73A24FFD6540'})
        self.driver.add_cookie({'name': 'xk.passport.info', 'value': '%7b%22UserId%22%3a1784957%2c%22UserName%22%3a%22wangxiaolei_123%22%2c%22Identity%22%3a200001%2c%22UserGroupID%22%3a4%2c%22SchoolId%22%3a430574%2c%22endDataStr%22%3anull%2c%22userFace%22%3a%2200001.jpg%22%7d'})
        self.driver.add_cookie({'name': 'xk.passport.uid', 'value': '1784957'})
        self.driver.add_cookie({'name': 'ASP.NET_SessionId', 'value': 'abfiiaq34b5y2nlyqx1kjefh'})
        #刷新
        self.driver.refresh()

        # locator = (By.CSS_SELECTOR, 'div#biao')
        # 一个只要一个符合条件的元素加载出来就通过
        # WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located(locator))

    def get_url(self):
        """返回浏览器的地址"""
        return BASE_URL

    def find_element(self, by, value):

        """
        这里添加了一个OVER_TIME作为查找元素的超时次数，根据系统的实际情况设置OVER_TIME的大小
        """

        for i in range(OVER_TIME):
            try:
                return self.driver.find_element(by=by, value=value)
            except Exception, e:
                print e

        def find_elements(self, by, value):

            """与find_element一致"""

        for i in range(OVER_TIME):
            try:
                return self.driver.find_elements(by=by, value=value)
            except Exception, e:
                print e

    def find_display_elements(self, by, value):

        """
        查找状态为displayed的元素集合，当查找一类元素时，
        经常出现有些元素是不可见的情况，此函数屏蔽那些不可见的元素
        """
        for i in range(OVER_TIME):
            try:
                elements = self.driver.find_elements(by=by, value=value)
                num = elements.__len__()
            except Exception, e:
                print e
                time.sleep(1)
            if num >= 1:
                break
        display_element = []  # 将可见的元素放到列表中， 并返回
        for j in range(num):
            element = elements.__getitem__(j)
            if element.is_displayed():
                display_element.append(element)
        return display_element

    def is_element_present(self, By, Value):
        """判断元素是否存在"""
        try:
            self.driver.find_element(by=By, value=Value)
            return True
        except Exception, e:
            print e
        return False

    def close(self):
        self.driver.close()

    def quit(self):
        u"""退出浏览器"""
        self.driver.quit()


if __name__ == "__main__":

    t0 = time.time()
    page = Driver()
    t1 = time.time()
    print 'cost ' + str(t1 - t0)
    page.start()
    t2 = time.time()
    print 'cost ' + str(t2 - t1)

    # 当前主页面
    currentWindow = page.driver.current_window_handle
    print 'main page: ' + currentWindow
    """
    # 登陆按钮，跳转到登陆界面
    loginHref = page.driver.find_element_by_link_text('登录')
    loginHref.click()
    time.sleep(1)
    # 新窗口
    # print page.driver.page_source
    # 开始登陆

    userName = page.driver.find_element_by_id('username')
    userPass = page.driver.find_element_by_name('password')
    loginBtn = page.driver.find_element_by_id('CommonLogin')
    # 填值
    userName.send_keys('13789826822')
    userPass.send_keys('13789826822')
    loginBtn.click()
    # 登陆完成
    """
    js = 'window.open("' + MAIN_PAGE1 + '")'
    page.driver.execute_script(js)
    print 'currentPage' + page.driver.current_window_handle

    # 切换视窗
    for handle in page.driver.window_handles:
        if handle != currentWindow:
            print 'switch to ', handle
            page.driver.switch_to.window(handle)
        else: # 关闭登陆页
            page.driver.close()

    currentWindow = page.driver.current_window_handle

    print page.driver.current_url

    # 点击一下页
    for i in range(1, 2):
        # 滚动条
        js = 'window.scrollTo(0, 400)'
        page.driver.execute_script(js)
        time.sleep(0.666)
        # 开始解析当前页面
        articleLinks = page.driver.find_elements(By.CSS_SELECTOR, 'a.high_light')
        #先打开第一页全部链接（每页10个）
        for idx, article in enumerate(articleLinks):
            link = article.get_attribute('href')
            print 'open %s with %s' %(id, article.text)
            js = 'window.open("' + link + '")'
            # 打开连接新窗口
            page.driver.execute_script(js)
            time.sleep(1.366)
        #end for
        # 切换到文件下载页面
        for handle in page.driver.window_handles:
            if handle != currentWindow:
                print 'switch to ', handle
                page.driver.switch_to.window(handle)
                time.sleep(1.333)
                js = 'window.scrollTo(0, $(document).height() - 100)'
                page.driver.execute_script(js)
                time.sleep(1.666)

                #开始下载
                downBtn = page.find_display_elements(By.CSS_SELECTOR,'a#btnSoftDownload.btn')
                downBtn[0].click()
                time.sleep(5.333)
                #关闭当前页
                page.driver.close()
        # end for

        # 点击下一页
        nextPage = page.driver.find_element_by_link_text('下页')
        nextPage.click()
        time.sleep(1.333)

    """
    links = page.find_display_elements(By.CSS_SELECTOR, 'a.ulink')
    for link in links:
        linkUrl = link.get_attribute('href')
        # print link.text, '[', linkUrl, ']'

    for idx, link in enumerate(links[:10]):
        linkUrl = link.get_attribute('href')
        title = link.text
        # 只需要匹配某一个电视剧名字
        if title.find(u'超女') != -1 or True:
            # 依次打开
            js = 'window.open("' + linkUrl + '")'
            page.driver.execute_script(js)

            time.sleep(1.22)
            print 'only open ' + str(idx) + ' page to test'
            # break
        # 这里并不会切换到新页面
        # print 'current : ' + page.driver.current_window_handle

    for handle in page.driver.window_handles:
        if handle != currentWindow:
            # print 'switch to ', handle
            page.driver.switch_to.window(handle)
            print page.driver.current_window_handle
            # print 'get something from this page'

            print '==========Xunlei Download=========='
            aLinks = page.find_display_elements(By.CSS_SELECTOR, 'div#Zoom td a')
            for aLink in aLinks:
                print aLink.text

            print '==========Web Flashplayer========='
            xiguaLinks = page.find_display_elements(By.CSS_SELECTOR, 'div#Zoom li a')
            for xiguaLink in xiguaLinks:
                print xiguaLink.text, xiguaLink.get_attribute('href')
            time.sleep(1.33)
            # 关闭当前选项卡
            page.driver.close()

    print 'main page left...'
    # 切换到main
    page.driver.switch_to.window(currentWindow)
    time.sleep(2)
    # by xpath
    # nextPage = page.find_element(By.XPATH, '//div[@class="x"]/a[0]')
    # by link text
    nextPage = page.driver.find_element_by_link_text('下一页')
    nextPage.click()
    """
