# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OVER_TIME = 2
# BASE_URL = "https://www.dy2018.com/html/gndy/dyzz/index.html"
BASE_URL = "https://www.dy2018.com/html/tv/oumeitv/"


class Driver(object):
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
                    'images': 2,
                    'javascript': 2
                },
                'profile.default_content_settings.popups': 0,
                'download.default_directory': 'F:\\个人\\english-doc-7degree'
            }
            options.add_experimental_option('prefs', prefs)
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

    for i in range(1,3):
        # 当前主页面
        currentWindow = page.driver.current_window_handle
        print 'main page: ' + currentWindow

        links = page.find_display_elements(By.CSS_SELECTOR, 'a.ulink')
        for link in links:
            linkUrl = link.get_attribute('href')
            # print link.text, '[', linkUrl, ']'

        for idx, link in enumerate(links):
            linkUrl = link.get_attribute('href')
            title = link.text
            # 只需要匹配某一个电视剧名字
            # if title.find(u'超女') != -1 or True:
            if True:
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

        time.sleep(1.333)

    # end for



