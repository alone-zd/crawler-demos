"""
# @Time: 2020/4/2 11:18
# @Author: Alone
# @File: jdmobile_spider.py
爬取京东的apple，华为，小米的手机信息

"""
from pyquery import PyQuery as pq
import requests
import time
import xlwt


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'cookie': 'shshshfpa=e4eb998f-54b8-eb4b-d3c9-d47718775d0c-1569764357; qrsc=3; pinId=wzK2JnQyXHVmvUD2AZqPpbV9-x-f3wj7; __jdu=737614119; shshshfpb=csfTaYg5JOqsHlAAmVr84JQ%3D%3D; user-key=8c2ec8ab-18b2-4089-8608-e97c843eeb0d; cn=0; unick=%E6%B9%AE%E8%8A%B1%E7%9F%AD%E6%9A%82; _tp=vW6hnrf85aq6cfpyBUS%2Bc58LR190IHqDEnB1sfDcqZ8%3D; _pst=jd_4afbb137447b9; pin=jd_4afbb137447b9; TrackID=1xOCQ3iIDVaS15UDuTkfwUEBb17ql5dqEAxqWVZY7ZjnLFLe-o4pXKfWl_-O231ep_Nzq_aC7fLF3WibyLjT_4vvT4Ks6v3c9SxLGP9Yb1tA; areaId=27; ipLoc-djd=27-2376-50231-0; unpl=V2_ZzNtbUFRQxNyDBIEf0wIBWJREg8SAxAUcg0RUiscXAJgVhtcclRCFnQUR1FnGF8UZwMZXktcRxZFCEdkeBBVAWMDE1VGZxBFLV0CFSNGF1wjU00zQwBBQHcJFF0uSgwDYgcaDhFTQEJ2XBVQL0oMDDdRFAhyZ0AVRQhHZH0bWgJnBhJdSmdzEkU4dlR5Hl0MYTMTbUNnAUEpDERUfxteSGEBFFpCUkMVfThHZHg%3d; __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_271765ea5de14c1caeb064f7a4166d80|1585798133353; PCSYCityID=CN_0_0_0; xtest=9761.cf6b6759; __jdc=122270672; rkv=V0800; 3AB9D23F7A4B3C9B=EDVZTX6GLQJY2E4PE5BLBBML7PW2AG6NYHFNLIWXX7K6HOGWYYAVXQCNXRMIFVDAR3P4XDA2XEIKDLAIRSHRQFONV4; shshshfp=b36e283af299f4987d883ed1a9bccccc; __jda=122270672.737614119.1569764355.1585800323.1585819139.34; __jdb=122270672.2.737614119|34.1585819139; shshshsID=afd048eb837305a80e1e5c072e3eff9a_2_1585819511305'
}
url = 'https://search.jd.com/Search?keyword=apple&enc=utf-8&wq=apple&pvid=25cd108f613c43249bd1d4badcca2e5b'
def get_one_page(url):
    try:
        result = requests.get(url, headers=headers)
        if result.status_code == 200:
            html = result.content
            html_doc = str(html, 'utf-8')
            return html_doc
        return None
    except Exception:
        return None


def parse_one_page(html):
    """
    使用pyquer处理html，根据css选择器得到所需数据
    :param html:
    :return: 可迭代的数据
    """
    doc = pq(html)
    ul = doc('.gl-warp.clearfix')
    liList = ul('.gl-item')
    for li in liList.items():
        # 商品
        product = li('div > div.p-name.p-name-type-2 > a > em')[0].text
        # 京东精选
        if product == None:
            product = li('div > div.p-name.p-name-type-2 > a').attr('title')
        # 价格
        price = li('div > div.p-price > strong > i').text()
        # 商家
        seller = li('div > div.p-shop > span > a').text()
        yield {
            'product': product,
            'price': price,
            'seller': seller
        }


if __name__ == '__main__':
    urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&page={}&s=55&click=0'
                .format(i) for i in range(1,8,2)]
    head = ['排名', '产品', '价格', '卖家']
    book = xlwt.Workbook(encoding='utf-8')
    sheet_all = book.add_sheet('所有手机排行')
    sheet_apple = book.add_sheet('Apple手机')
    sheet_huawei = book.add_sheet('华为手机')
    sheet_xiaomi = book.add_sheet('小米手机')
    # 设置头部
    for h in range(len(head)):
        sheet_all.write(0, h, head[h])
        sheet_apple.write(0, h, head[h])
        sheet_huawei.write(0, h, head[h])
        sheet_xiaomi.write(0, h, head[h])
    i = 1
    apple_i = 1
    huawei_i = 1
    xiaomi_i = 1
    for url in urls:
        mobile_infos = parse_one_page(get_one_page(url))
        for mobile_info in mobile_infos:
            print(mobile_info)
            sheet_all.write(i, 0, str(i))
            sheet_all.write(i, 1, mobile_info['product'])
            sheet_all.write(i, 2, mobile_info['price'])
            sheet_all.write(i, 3, mobile_info['seller'])
            # 苹果
            if mobile_info['product'].lower().find('apple') != -1:
                sheet_apple.write(apple_i, 0, str(i))
                sheet_apple.write(apple_i, 1, mobile_info['product'])
                sheet_apple.write(apple_i, 2, mobile_info['price'])
                sheet_apple.write(apple_i, 3, mobile_info['seller'])
                apple_i += 1
            # 华为
            if mobile_info['product'].lower().find('华为') != -1:
                sheet_huawei.write(huawei_i, 0, str(i))
                sheet_huawei.write(huawei_i, 1, mobile_info['product'])
                sheet_huawei.write(huawei_i, 2, mobile_info['price'])
                sheet_huawei.write(huawei_i, 3, mobile_info['seller'])
                huawei_i += 1
            # 小米
            if mobile_info['product'].lower().find('小米') != -1:
                sheet_xiaomi.write(xiaomi_i, 0, str(i))
                sheet_xiaomi.write(xiaomi_i, 1, mobile_info['product'])
                sheet_xiaomi.write(xiaomi_i, 2, mobile_info['price'])
                sheet_xiaomi.write(xiaomi_i, 3, mobile_info['seller'])
                xiaomi_i += 1
            i += 1
    book.save('phone_rank.xls')