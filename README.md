
## Scrapy 爬取京东商城华为全系列手机评论/可视化分析:


    大致分析了下京东评论 相同手机型号的产品用的评论都是一样的,所以每个型号的爬一个就可以了; 
    每一个评论最多只能爬100页,每页10条, 加上好中差评 大概能有2000多条不重复的评论
    {productId}就是对应产品的productId;  
    {score}对应全部/好/中/差评 0:全部评价  1:差评  2:中评  3:好评
    
#### 评论爬取url:
    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?productId={productId}&score={score}&sortType=5&page={page}&pageSize=10&isShadowSku=0&rid=0&fold=1'


###
### 我是根据这里,每个型号的找一个主页,爬取评论
##
![python](https://github.com/srp527/JD_Parse/blob/master/jd_parse/img/1.png)
## 
### 对应的html代码,用beautisoup分析网页,得到手机型号和herf
![python](https://github.com/srp527/JD_Parse/blob/master/jd_parse/img/2.png)

##
#### 代码实现:

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
##   
#### 得到一个字典, key是对应url(手机详情页) , value是productId和手机型号:
    {'https://item.jd.com/5544068.html': ['5544068', 'HUAWEI Mate 10'], 
    'https://item.jd.com/5826236.html': ['5826236', 'HUAWEI Mate 10 Pro'], 
    'https://item.jd.com/3888284.html': ['3888284', 'HUAWEI Mate 9'], 
    'https://item.jd.com/3749093.html': ['3749093', 'HUAWEI Mate 9 Pro'], 
    'https://item.jd.com/6946605.html': ['6946605', 'HUAWEI P20'], 
    'https://item.jd.com/6946625.html': ['6946625', 'HUAWEI P20 Pro'], 
    'https://item.jd.com/5148387.html': ['5148387', '麦芒6 极光蓝'], 
    'https://item.jd.com/8026730.html': ['8026730', 'HUAWEI nova 3'], ...}

### Start_requests:这里用的方法比较简单就是遍历循环,根据url三个参数,
### 爬取每个手机型号的,好中差评评论,最后通过pipelines存入mongodb:

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

#### 爬到的数据
![python](https://github.com/srp527/JD_Parse/blob/master/jd_parse/img/2.png)

#### 代码还有不完善的地方,京东不同产品评论数据返回的格式有差异,有很多评论没有抓到


## 未完待续...
