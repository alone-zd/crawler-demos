"""
# @Time: 2020/3/27 16:50
# @Author: Alone
# @File: WeatherSpider.py
# 爬取中国天气的固定城市的天气
http://www.weather.com.cn/
# var dataSK = {nameen: "beijing", cityname: "北京", city: "101010100", temp: "13", tempf: "55", WD: "西风", wde: "W",…}
"""
import scrapy
import json
import re
from scrapy.http import Request
from myscrapy.items import WeatherItem

def str_to_headers(file):
    header_dict = {}
    f = open(file, 'r')
    header_txt = f.read()
    headers = re.split('\n', header_txt)
    for header in headers:
        result = re.split(':', header, maxsplit=1)
        header_dict[result[0]] = result[1]
    f.close()
    return header_dict


class WeatherSpider(scrapy.Spider):
    name = 'WeatherSpider'

    def start_requests(self):
        headers = str_to_headers('header.txt')
        return [
            Request(url='http://d1.weather.com.cn/sk_2d/101010100.html?_=1585298869053', headers=headers)
        ]

    def parse(self, response):
        result = re.sub('var[ ]+dataSK[ ]+=[ ]+','',response.body.decode('utf-8'))
        json_dict = json.loads(result)
        weather_item = WeatherItem()
        for key, value in json_dict.items():
            weather_item.fields[key] = scrapy.Field()
            weather_item[key] = value
        return weather_item

