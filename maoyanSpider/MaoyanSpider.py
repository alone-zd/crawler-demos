"""
# @Time: 2020/3/29 22:00
# @Author: Alone
# @File: MaoyanSpider.py
# 技术：urllib3
# 猫眼电影Top100榜单爬虫
# https://maoyan.com/board/4
"""
from urllib3 import *
import re
import json
import time


disable_warnings()
http = PoolManager()


def getOnePage(url):
    """
    获取对应url下的html
    :param url:
    :return: html的文本数据
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }
        response = http.request('GET', url, headers=headers)
        data = response.data.decode('utf-8')
        if response.status == 200:
            return data
        return None

    except Exception:
        raise None


def parseOnePage(html):
    """
    将html进行正则匹配。获取需要的数据
    :param html:
    :return: 处理好数据的迭代器
    """
    # 详细正则匹配见web_demo.html
    pattern = re.compile('<dd>.*?board-index.*?(\d+)</i>.*?data-src="(.*?)".*?name">'
                         '<a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],  # 电影索引
            'image': item[1],  # 图像url
            'title': item[2],  # 标题
            'actor': item[3].strip()[3:],  # 导演
            'time': item[4].strip()[5:],  # 上映时间
            'sorce': item[5]+item[6]  # 评分
        }


# 保存数据
def save(content):
    with open('bord.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def getBord(offset):
    url = 'https://maoyan.com/board/4?offset=' + str(offset)
    html = getOnePage(url)
    for item in parseOnePage(html):
        print(item)
        save(item)

# 对10页数据进行爬取
for i in range(10):
    getBord(offset=i * 10)
    time.sleep(1)

