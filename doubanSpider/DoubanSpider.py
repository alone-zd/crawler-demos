"""
# @Time: 2020/3/31 10:13
# @Author: Alone
# @File: DoubanSpider.py
# 抓取豆瓣Top250的书名，作者，发行时间，价格
https://book.douban.com/top250?start=0
requests,xpath
注意： 这里我在进行爬取时，发现他已经设置了反扒，返回码为418，我使用了临时的ip地址，和header，解决了这个问题
"""
from lxml import etree
import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
proxies = {
    'http':'http://60.182.34.230:34942',
    'https': 'https://60.182.34.230:34942'
}
def get_one_page(url):
    """
    获取指定url下的html
    :param url:
    :return: html的文本
    """
    try:
        res = requests.get(url, proxies=proxies, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except Exception:
        return None


def parse_one_page(html):
    selector = etree.HTML(html)
    # 选出tr节点
    items = selector.xpath('//tr[@class="item"]')
    for item in items:
        book_infos = item.xpath('td/p/text()')[0]
        yield {
            'name': item.xpath('td/div/a/@title')[0],
            'url': item.xpath('td/div/a/@href')[0],
            'author': book_infos.split('/')[0],
            'publisher': book_infos.split('/')[-3],
            'date': book_infos.split('/')[-2] ,
            'price': book_infos.split('/')[-1]
        }


def save(content):
    with open('Top250books', 'at', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def getTop250(url):
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        save(item)

urls = ['https://book.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]

for url in urls:
    getTop250(url)

