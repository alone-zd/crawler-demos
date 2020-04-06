"""
# @Time: 2020/3/31 14:32
# @Author: Alone
# @File: novel_spider.py
# 爬取起点小说的小说信息，保存在excel里面
request, xpath, xlwt
https://www.qidian.com/all?page=1
"""
import xlwt
import requests
from lxml import etree
import time


def get_one_page(url):
    html = requests.get(url)
    selector = etree.HTML(html.text)
    infos = selector.xpath('//ul[@class="all-img-list cf"]/li')
    for info in infos:
        style_1 = info.xpath('div[2]/p[1]/a[2]/text()')[0]
        style_2 = info.xpath('div[2]/p[1]/a[3]/text()')[0]
        yield {
            'title': info.xpath('div[2]/h4/a/text()')[0],
            'author': info.xpath('div[2]/p[1]/a[1]/text()')[0],
            'style': style_1 + '.' + style_2,
            'complete': info.xpath('div[2]/p[1]/span/text()')[0],
            'introduce': info.xpath('div[2]/p[2]/text()')[0].strip()
        }


def save():
    """
    创建excel表格，保存相关数据
    :return:
    """
    header = ['标题','作者','类型','完成度', '介绍']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('小说')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    # 前10页url
    urls = ['https://www.qidian.com/all?page={}'.format(str(i)) for i in range(1, 11)]
    i = 1
    for url in urls:
        novels = get_one_page(url)
        for novel in novels:
            print(novel)
            sheet.write(i, 0, novel['title'])
            sheet.write(i, 1, novel['author'])
            sheet.write(i, 2, novel['style'])
            sheet.write(i, 3, novel['complete'])
            sheet.write(i, 4, novel['introduce'])
            i += 1
    book.save('novels.xls')

save()


