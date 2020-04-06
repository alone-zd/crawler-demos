"""
# @Time: 2020/3/29 17:36
# @Author: Alone
# @File: NovelSpider.py
# 技术： urllib ,re
# 爬取斗破苍穹的所有目录及内容
# http://www.doupoxs.com/
"""
from urllib import request
import re


headers = {
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

def getCatelogs(url):
    """
    获取每个章节对应的标题的url
    :param url: 爬取目标小说的url
    :return: 每个标题对应的url和标题名称
    """
    req = request.Request(url=url, headers=headers, method='GET')
    response = request.urlopen(req)

    # 返回数据
    result = []
    if response.status == 200:
        html = response.read().decode('utf-8')
        # 得到所有li标签
        liList = re.findall('<li>.*</li>', html)

        for li in liList:
            # 过滤出url和标题
            # <a href="/doupocangqiong/1.html" title="第一章 陨落的天才" class="">第一章 陨落的天才</a>
            g = re.search('href="([^>"]*)"[\s]*title="([^>"]*)"', li)
            if g != None:
                # 得到完整的url
                url = 'http://www.doupoxs.com/' + g.group(1)
                # 得到title
                title = g.group(2)

                chapter = {'title':title, 'url':url}
                result.append(chapter)
        return result


def getChapterContent(chapters):
    """
    将对应这跟信息写入novels的文件夹
    :param chapters: 标题和url组成的字典
    :return:
    """
    for chapter in chapters:
        req = request.Request(url=chapter['url'], headers=headers, method='GET')

        response = request.urlopen(req)
        if response.status == 200:
            f = open('novels/'+chapter['title']+'.txt', 'a')
            contents = re.findall('<p>(.*?)</p>', response.read().decode('utf-8'))
            for content in contents:
                f.write(content+'\n')
            f.close()
            print(chapter['title'])

getChapterContent(getCatelogs('http://www.doupoxs.com/doupocangqiong/'))

