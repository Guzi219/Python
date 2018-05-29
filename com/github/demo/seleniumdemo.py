# -*- coding: utf-8 -*-
"""
测试selenium自动化渲染js
"""
from selenium import webdriver


# browser = webdriver.Chrome()
# browser.get("http://www.baidu.com")
# browser.find_element_by_id("kw").send_keys("selenium")
# browser.find_element_by_id("su").click()
# browser.quit()
from selenium.webdriver.chrome.options import Options


def main():
    # driver = webdriver.Chrome()
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('http://www.well1000.cn/stdown/yingyu/122541.html')
    # driver.find_element_by_id('search_term').send_keys('.')
    driver.execute_script("shi")
    # driver.find_element_by_id('search').click()
    driver.implicitly_wait(30)
    links = driver.find_elements_by_css_selector('#biao a')
    for link in links:
        print 'url ', link.get_attribute('href')
        print 'name ', link.text

    # 关闭当前网页，如果只有一个页面，会关闭浏览器
    driver.close()
    # driver.quit()
    # print countries


if __name__ == '__main__':
    main()
