# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy import Item,Field

class JdParseItem(Item):
    # define the fields for your item here like:
    # name = Field()
    id = Field()               #用户ID
    model = Field()            #手机型号
    nickname = Field()         #昵称
    userLevelName = Field()    #用户级别
    content = Field()          #内容
    productColor = Field()     #产品颜色
    productSize = Field()      #产品类型(标准版)
    productSales = Field()     #产品配置 (6G+128G) productSales":[{"dim":3,"saleName":"选择内存","saleValue":"6GB+64GB"}],
    userClientShow = Field()   #用户客户端
    score = Field()            #评论类型
    creationTime = Field()     #评论日期
