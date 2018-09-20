# -*- coding:utf-8 -*- 
__author__ = 'SRP'

import collections

import pandas as pd
from matplotlib import pyplot as plt
from pyecharts import WordCloud

from jd_visual.mongodb import MongoPipeline1

db = MongoPipeline1()
datas = MongoPipeline1.from_mongo(db)
db.close_mongo()

#爬的所有数据
comments = list(datas)

def word_clout(title,content_list,num_list,word_size_range):
    '''词云图'''

    wordcloud = WordCloud(width=1400,height=900)

    wordcloud.add("",content_list,num_list,word_size_range=word_size_range,shape='pentagon')
    out_file_name = './imgs/'+title+'.html'
    wordcloud.render(out_file_name)

#转成 DataFrame 并存入cvs文件中
def to_csv(comments,line_list,name):
    '''
    :param comments:  dict数据
    :param line_list: 要保存列的名称
    :return:
    '''
    data = pd.DataFrame(list(comments))
    del data['_id']
    data = data[line_list]
    data.to_csv('./cvs/'+name+'.cvs')

line_list = ['model','content','score','creationTime','nickname','productColor','productSales','productSize','userClientShow','userLevelName']
# to_csv(comments,line_list,name)


# model_list = ['HUAWEI Mate 10', 'HUAWEI Mate 10 Pro', 'HUAWEI Mate 9', 'HUAWEI Mate 9 Pro', 'HUAWEI P20',
#               'HUAWEI P20 Pro', '麦芒6 极光蓝', 'HUAWEI nova 3', 'HUAWEI nova 3i', 'nova 3e',
#               'HUAWEI nova 2 Plus', 'nova 2S', ' 畅享8', '畅享8 Plus', '畅享8e', '畅享7 Plus', '畅享7S',
#               'HUAWEI WATCH 2 Pro', 'HUAWEI WATCH 2', '华为儿童手表', '华为平板M3', '华为路由Q1']
#
# data = pd.read_csv('./cvs/all_comments.csv')
# a = data.groupby('model').count()
# for i in model_list:
#     a = data[data['model']==i]
#     a.to_csv('./cvs/'+i+'.csv')

data = pd.read_csv('./cvs/HUAWEI P20 Pro.csv')






#方式二:
#把数据归类, 相同型号的评论放到一起
# dic = {}
# for comment in comments:
#     del comment['_id']
#     if comment['model'] not in dic.keys():
#         dic[comment['model']] = []
#     dic[comment['model']] += [comment]

# print(dic.keys()) #dict_keys(['HUAWEI Mate 10', 'HUAWEI Mate 10 Pro', 'HUAWEI Mate 9', 'HUAWEI Mate 9 Pro', 'HUAWEI P20', 'HUAWEI P20 Pro', '麦芒6 极光蓝', 'HUAWEI nova 3', 'HUAWEI nova 3i', 'nova 3e', 'HUAWEI nova 2 Plus', 'nova 2S', ' 畅享8', '畅享8 Plus', '畅享8e', '畅享7 Plus', '畅享7S', 'HUAWEI WATCH 2 Pro', 'HUAWEI WATCH 2', '华为儿童手表', '华为平板M3', '华为路由Q1'])
# for key in dic.keys():
#     for comment in dic[key]:




#待统计参数
#生成好评的词云，并且获取关键字
# 生成中评的词云，并且获取关键字
# 生成差评的词云，并且获取关键字
# 分析购买该商品不同颜色的比例，生成柱状图
# 分析购买该商品不同配置的比例，生成柱状图
# 分析该商品的销售数量和评论数量和时间的关系，生成时间则线图
# 分析该商品不同省份购买的的比例，生成柱状图
# 分析该商品不同渠道的销售比例，生成柱状图