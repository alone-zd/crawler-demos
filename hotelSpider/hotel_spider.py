"""
# @Time: 2020/3/31 15:56
# @Author: Alone
# @File: hotel_spider.py
# 获取马蜂窝上一个酒店的信息
"""
from bs4 import BeautifulSoup
import requests
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}


def save_house_image(url, name):
    r = requests.get(url)
    name = str.replace(name, '/', '')
    with open('images/' + name, 'wb') as f:
        f.write(r.content)


def get_info(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')
    # 提取标题
    title = soup.find(class_='main-title').h1.text
    # 地址
    address = soup.find(class_='location').span.text.split('：')[1]
    # 图像url
    image_url = soup.find(class_='intro-bd clearfix').img['src']
    # 体验感觉
    feels = soup.find(class_='t').text
    # 评分
    score = soup.find(class_='score').text

    info = {
        'title': title,
        'address': address,
        'image_url': image_url,
        'feels': feels,
        'score': score
    }
    save_house_image(image_url, title+'.png')
    print(info)
    return info


if __name__ == '__main__':
    url = 'http://www.mafengwo.cn/hotel/7377025.html'
    info = get_info(url)
    f = open('./houses.txt', 'a+', encoding='utf-8')
    f.write(json.dumps(info, ensure_ascii=False)+ '\n')
    f.close()

