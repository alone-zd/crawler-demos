"""
# @Time: 2020/4/4 22:55
# @Author: Alone
# @File: image_search_spider.py
 抓取百度图片中的图片(异步抓取),每次30张
"""
import random
import string
import requests
import os
import json


word = input('请输入搜索关键字：')
# 随机生成8位目录名
dir_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
print('图像文件保存在', dir_name, '目录中')
# 保存文件
os.mkdir(dir_name)
max_value = 50
# 图像当前索引
current_value = 0
# 图像文件名
image_index = 1
while current_value < max_value:
    print(word)
    result = requests.get('https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=%E7%8C%AB&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={}&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn={}&rn=30&gsm=5a&1586082133025='.format(word, current_value))
    json_str = result.content
    json_doc = str(json_str, 'utf-8')

    image_result = json.loads(json_doc)
    data = image_result['data']
    for record in data:
        url = record.get('middleURL')
        if url != None:
            print('正在下载图片：', url)
            r = requests.get(url)
            # 构造图片名称
            filename = dir_name + '/' + str(image_index).zfill(6) + '.png'
            with open(filename, 'wb') as f:
                f.write(r.content)
            image_index += 1
    current_value += 30
