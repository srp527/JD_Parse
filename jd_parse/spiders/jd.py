# -*- coding: utf-8 -*-
import re
import json
import time

import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy import Spider,Request

from jd_parse.items import JdParseItem

class JdSpider(scrapy.Spider):
    name = "jd"
    allowed_domains = ["www.jd.com"]

    start_urls = ['https://item.jd.com/5544068.html']  #score #0:全部评价  1:差评  2:中评  3:好评


    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={productId}&score={score}&sortType=5&page={page}&pageSize=10&isShadowSku=0&rid=0&fold=1'
    # haop_url =   'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6955&productId=6946627&score=3&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    # zhongp_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6955&productId=6946627&score=2&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'
    # chap_url =   'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6955&productId=6946627&score=1&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'

    response = requests.get(start_urls[0])
    soup = BeautifulSoup(response.content, 'lxml')
    content = soup.find_all('div', class_='erji')
    dic = {}
    model = ''
    for a in content:
        a_label = a.find_all('a')
        for href in a_label:
            productId = re.compile('\d+').findall(href.get('href'))[0]
            dic['https:' + href.get('href')] = [productId, href.get_text()]
    # print('------->',dic)

    def start_requests(self):
        for k,v in self.dic.items():
            productId = v[0]
            global model
            model = v[1]

            for score in range(4):
                page = 0
                while page < 101:
                    yield Request(self.comment_url.format(productId=productId,score=score,page=page),self.parse,dont_filter=True)
                    page += 1
                    time.sleep(1)


    def parse(self, response):
        # print('--->',response.text)
        # result = re.sub('fetchJSON_comment98vv6955\(','',response.text)
        # result = re.sub('\);', '', result)
        datas = json.loads(response.text)['comments']
        if datas:
            for data in datas:
                item = JdParseItem()
                for field in item.fields:
                    if field in data.keys():
                        item['model'] = model
                        if field == 'productSales':
                            item[field] = data.get(field)[0]['saleValue']
                        else:
                            item[field] = data.get(field)
                yield item




