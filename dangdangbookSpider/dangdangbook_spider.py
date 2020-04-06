"""
# @Time: 2020/4/2 8:26
# @Author: Alone
# @File: dangdangbook_spider.py
爬取当当网，有关python的所有的信息
http://search.dangdang.com/?key=python&page_index=1
"""
from pyquery import PyQuery as pq
import requests


def get_one_page(url):
    """
    获取url下的html页面
    :param url:
    :return: 页面的文本信息
    """
    try:
        reslut = requests.get(url)
        if reslut.status_code == 200:
            return reslut.text
        return None
    except Exception:
        return None


def parse_one_page(html):
    doc = pq(html)
    ul = doc('.bigimg')
    liList = ul('li')
    for li in liList.items():
        a = li('a:first-child')
        # 图书主页的url
        href = a[0].get('href')
        # 标题
        title = a[0].get('title')

        span = li('.search_now_price')
        # 价格
        price = span[0].text[1:]

        p = li('.search_book_author')
        # 作者
        author = p('a:first-child').text()

        # 出版日期
        date = p('span:nth-child(2)').text()[1:]
        # 出版社
        publisher = p('span:nth-child(3) > a').text()
        # 评论数
        comments = li('.search_comment_num').text()[:-3]
        # 简介
        detail = li('.detail').text()

        yield {
            'href': href,
            'title': title,
            'price': price,
            'author': author,
            'date': date,
            'publisher': publisher,
            'comments': comments,
            'detail': detail
        }


if __name__ == '__main__':
    urls = ['http://search.dangdang.com/?key=python&page_index={}'.format(str(i)) for i in range(1,4)]
    for url in urls:
        book_infos = parse_one_page(get_one_page(url))
        for book_info in book_infos:
            print(book_info)

