"""
# @Time: 2020/4/2 20:05
# @Author: Alone
# @File: douban_music_spider.py
抓取豆瓣音乐的top25榜单(多线程)
获取音乐名字，作者，流派，发行时间
https://music.douban.com/top250?start=0
技术：requests, Beautiful, re, css, threading
"""
from datetime import datetime

import requests
from bs4 import BeautifulSoup
import re
import csv
import threading
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
lock = threading.Lock()


def get_url():
    """
    对线程进行加锁，并防止多次读取第一个url
    :return:
    """
    global urls
    lock.acquire()
    if len(urls) == 0:
        lock.release()
        return ""
    else:
        url = urls[0]
        del urls[0]
    lock.release()
    return url

def get_url_music(url, thread_name):
    """
    获取主页面每个音乐对应详情页的href，即跳转链接
    :param url: 主页面的url
    :return:
    """
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    aTags = soup.find_all('a', attrs={'class': 'nbg'})
    for aTag in aTags:
        get_music(aTag['href'], thread_name)


def get_music(url, thread_name):
    """
    对详情页中需要获取的元素进行定位并获取
    :param url: 详情页跳转链接
    :param thread_name: 线程名
    :return:
    """
    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.text, 'lxml')
    # 专辑名称
    name = soup.find(attrs={'id': 'wrapper'}).h1.span.text
    # 表演者
    author = soup.find(attrs={'id': 'info'}).find('a').text
    # 流派
    style = re.findall('<span class="pl">流派:</span>&nbsp;(.*?)\n[ ]*<br />', html.text, re.S)
    if len(style) == 0:
        style = '未知'
    else:
        style = style[0].strip()
    # 发行时间
    time = re.findall('发行时间:</span>&nbsp;(.*?)[ ]*<br />', html.text, re.S)[0].strip()
    # 评分
    score = soup.find(class_='ll rating_num').text
    info = {
        'name': name,
        'author': author,
        'style': style,
        'time': time,
        'score': score
    }
    print(thread_name, info)


class SpiderThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while True:
            url = get_url()
            if url != "":
                get_url_music(url, self.name)
            else:
                break

if __name__ == '__main__':
    start_time = datetime.now()
    urls = ['https://music.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
    # 使用4个线程
    thread1 = SpiderThread('thread1')
    thread2 = SpiderThread('thread2')
    thread3 = SpiderThread('thread3')
    thread4 = SpiderThread('thread4')

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    # 确保线程执行完毕
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    end_time = datetime.now()
    print('需要时间', (end_time-start_time).seconds, '秒')



