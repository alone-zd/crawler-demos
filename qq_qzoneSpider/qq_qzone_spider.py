"""
# @Time: 2020/4/5 23:44
# @Author: Alone
# @File: qq_qzone_spider.py
# 使用selenium爬取qq空间的说说，需要进行滑块验证
https://user.qzone.qq.com/{}/311
"""
from selenium import webdriver
import time


# options = webdriver.ChromeOptions()
# options.add_argument('headless')
browser = webdriver.Chrome()
browser.maximize_window()

def get_info(qq):
    browser.get('https://user.qzone.qq.com/{}/311'.format(qq))
    browser.implicitly_wait(10)
    try:
        browser.find_element_by_id('login_div')
        flag = True
    except:
        flag = False
    if flag == True:
        browser.switch_to.frame('login_frame')
        browser.find_element_by_id('switcher_plogin').click()
        browser.find_element_by_id('u').clear()
        browser.find_element_by_id('u').send_keys('1281141257')
        browser.find_element_by_id('p')
        browser.find_element_by_id('p').send_keys('cleverlove.')
        browser.find_element_by_id('login_button').click()
        time.sleep(5)
    browser.implicitly_wait(3)
    browser.switch_to.frame('app_canvas_frame')
    contents = browser.find_elements_by_css_selector('.content')
    times = browser.find_elements_by_css_selector('.c_tx.c_tx3.goDetail')
    for content,t in zip(contents, times):
        data = {
            'time': t.text,
            'content': content.text
        }
        print(data)


if __name__ == '__main__':
    get_info('1281141257')