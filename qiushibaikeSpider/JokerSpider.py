"""
# @Time: 2020/3/30 8:57
# @Author: Alone
# @File: JokerSpider.py
# 技术：requests
# 爬取糗事百科的段子的用户，对应段子，好笑数和评论数
https://www.qiushibaike.com/text/
"""
import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}


def getJokes(url):
    result = []
    res = requests.get(url)

    # 用户昵称
    ids = re.findall('<h2>(.*?)</h2>', res.text, re.S)
    # 段子内容
    contents = re.findall('<div class="content">.*?<span>(.*?)</span>', res.text, re.S)
    # 好笑数
    laughs = re.findall('<span class="stats-vote"><i class="number">(.*?)</i>', res.text, re.S)
    # 评论数
    comments = re.findall('<i class="number">(.*?)</i>', res.text, re.S)
    for id,content,laugh,comment in zip(ids, contents, laughs, comments):
        info = {
            'id': id,
            'content': content,
            'laugh': laugh,
            'comment': comment
        }
        result.append(info)
    return result


urls = ['https://www.qiushibaike.com/text/{}'.format(str(page)) for page in range(1,31)]

for url in urls:
    jokeLists = getJokes(url)
    for joke in jokeLists:
        f = open('./jokes.txt', 'a+', encoding='utf-8')
        try:
            f.write(joke['id'] + '\n')
            f.write(joke['content']+'\n')
            f.write(joke['laugh']+'\n')
            f.write(joke['comment']+'\n')
            f.close()
        except UnicodeEncodeError:
            print('写入失败')