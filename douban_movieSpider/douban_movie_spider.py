"""
# @Time: 2020/4/3 11:31
# @Author: Alone
# @File: douban_movie_spider.py
# 抓取豆瓣电影top250每个电影的信息，保存到sqlite数据库
https://movie.douban.com/top250?start=0
"""
import requests
from lxml import etree
import sqlite3
import os
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}


def get_movie_url(url):
    """
    获取跳转到详情页的href
    :param url:
    :return:
    """
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    movie_urls = selector.xpath('//div[@class="hd"]/a/@href')
    for movie_url in movie_urls:
        get_movie_info(movie_url)


def get_movie_info(url):
    """
    对所需信息进行查询，并保存到sqlite数据库中
    :param url:
    :return:
    """
    html = requests.get(url, headers=headers)
    selector = etree.HTML(html.text)
    try:
        # 电影名称
        movie_name = selector.xpath('//*[@id="content"]/h1/span[1]/text()')[0]
        # 导演
        director = selector.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')[0]
        # 主演
        actors = selector.xpath('//*[@id="info"]/span[3]/span[2]')[0]
        actor = actors.xpath('string(.)')
        # 类型
        style = re.findall('<span property="v:genre">(.*?)</span>', html.text, re.S)[0]
        # 制片国家
        country = re.findall('<span class="pl">制片国家/地区:</span>(.*?)<br/>', html.text, re.S)[0]
        # 评分
        score = selector.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')[0]
        print(movie_name, director, actor, style, country, score)
        global id
        id += 1
        movie = (id, movie_name, director, actor, style, country, score)
        cursor.execute('''
            insert into movies(id, movie_name, director, actor, style, country, score) values(?,?,?,?,?,?,?)'''
                       ,movie)
        conn.commit()

    except Exception:
        return None


if __name__ == '__main__':
    id = 0
    db_path = 'movie.sqlite'
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        create table movies(
            id int not null, 
            movie_name char(50) not null, 
            director char(50) not null, 
            actor char(50) not null, 
            style char(50) not null, 
            country char(50) not null,
            score real not null
        );
    ''')
    conn.commit()
    urls = ['https://movie.douban.com/top250?start={}'.format(str(i)) for i in range(0,250,25)]
    for url in urls:
        get_movie_url(url)
    conn.close()