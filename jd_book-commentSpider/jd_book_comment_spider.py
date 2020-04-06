"""
# @Time: 2020/4/5 22:47
# @Author: Alone
# @File: jd_book_comment_spider.py
# 抓取京东商品的评论信息
https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=12417265&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1
"""
import requests
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}
proxies = {
    'https': '...'
}


index = 0
page_index = 0
flag = True
# 最大评论数
fetch_comment_count = 15
while flag:
    url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=12417265&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'.format(page_index)
    page_index += 1
    html = requests.get(url, headers=headers)

    text = str(html.content, encoding='iso-8859-1')
    json_str = text.replace('fetchJSON_comment98(', '')
    json_str = json_str.replace(')', '')
    json_str = json_str.replace('true', "true")
    json_str = json_str.replace('false', "false")
    json_str = json_str.replace('null', "null")
    json_str = json_str.replace(';', '')
    json_obj = json.loads(json_str)

    for i in range(0, len(json_obj['comments'])):
        try:
            comment = json_obj['comments'][i]['content'].encode(encoding='iso-8859-1').decode('GB18030')
            if comment != '此用户未填写评价内容':
                print('<',index+1,'>',comment)
                creationTime = json_obj['comments'][i]['creationTime']
                nickname = json_obj['comments'][i]['nickname'].encode(encoding='iso-8859-1').decode('GB18030')
                print(creationTime)
                print(nickname)
                print('------------------->')
                index += 1
        except:
            pass
        if index == fetch_comment_count:
            flag = False
            break



