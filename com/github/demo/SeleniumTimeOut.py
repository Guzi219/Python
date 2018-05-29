# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
"""
selenuim 三种等待时间
"""

t0 = time.time()
driver = webdriver.Chrome()
driver.implicitly_wait(8)  # 隐性等待和显性等待可以同时用，但要注意：等待的最长时间取两者之中的大者
driver.get('https://huilansame.github.io')
locator = (By.LINK_TEXT, 'CSDN')

try:
    WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located(locator))
    t1 = time.time()
    print str(t1 - t0)

    print driver.find_element_by_link_text('CSDN').get_attribute('href')
finally:
    driver.close()