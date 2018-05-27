# -*- coding:utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

OVER_TIME = 6
BASE_URL = "http://www.well1000.cn/xiazai/yingyu/148321.html"


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
                    # 'javascript': 2
                },
                'profile.default_content_settings.popups': 0,
                'download.default_directory': 'F:\\个人\\english-doc'
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
        t0 = time.time()
        self.driver.get(url)
        # 执行javaascript： shi() 得到下载地址
        # self.driver.execute_script("shi()")
        locator = (By.CSS_SELECTOR, 'div#biao')
        # 一个只要一个符合条件的元素加载出来就通过
        WebDriverWait(self.driver, 10, 0.5).until(EC.presence_of_element_located(locator))
        print 'cost ' + str(time.time() - t0)

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
    # print type(page.find_element(By.ID, 'biao'))
    link = page.find_element(By.CSS_SELECTOR, 'div#biao a')
    print 'url ', link.get_attribute('href')
    print 'name ', link.text
    link.click()
    # # ctrl+t 打开新标签页
    page.find_element(By.TAG_NAME, 'body').send_keys(Keys.COMMAND + 't')
    # js = " window.open('http://www.well1000.cn/stdown/yingyu/122545.html')"  # 可以看到是打开新的标签页 不是窗口
    # page.driver.execute_script(js)
    # 下载二遍
    # page.start('http://www.well1000.cn/stdown/yingyu/122545.html')
    # link = page.find_element(By.CSS_SELECTOR, 'div#biao a')
    # print 'url ', link.get_attribute('href')
    # print 'name ', link.text
    # link.click()

    # page.quit()
