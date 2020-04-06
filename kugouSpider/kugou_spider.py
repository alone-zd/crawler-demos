"""
# @Time: 2020/4/1 21:18
# @Author: Alone
# @File: kugou_spider.py
# 抓取酷狗网络红歌榜,保存到excel里面
https://www.kugou.com/yy/rank/home/1-23784.html
技术：requests， css选择器
"""
from bs4 import BeautifulSoup
import requests
import xlwt

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}


def get_info(url):
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, 'lxml')

    # 名次
    ranks = soup.select('span.pc_temp_num')
    # 歌曲和歌手
    songs = soup.select('div.pc_temp_songlist > ul > li > a')
    # 时长
    times = soup.select('span.pc_temp_tips_r > span')
    for rank, song, time in zip(ranks, songs, times):
        yield {
            'rank': rank.get_text().strip(),
            'singer': song.get_text().split('-')[0],
            'song': song.get_text().split('-')[1],
            'time': time.get_text().strip()
        }


def save():
    urls = ['https://www.kugou.com/yy/rank/home/{}-23784.html'.format(str(i)) for i in range(1, 11)]
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('酷狗网络红歌榜')
    titles = ['排名', '歌手', '歌曲', '时长']
    for i in range(4):
        sheet.write(0,i,titles[i])
    j=1
    for url in urls:
        msgs = get_info(url)
        for msg in msgs:
            print(msg)
            sheet.write(j, 0, msg['rank'])
            sheet.write(j, 1, msg['singer'])
            sheet.write(j, 2, msg['song'])
            sheet.write(j, 3, msg['time'])
            j += 1
    book.save('hot_songs.xls')


if __name__ == '__main__':
    save()