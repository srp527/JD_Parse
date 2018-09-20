# -*- coding:utf-8 -*- 
__author__ = 'SRP'

import pymongo

from jd_parse.settings import MONGO_DATABASE,MONGO_URI,MONGO_TABLE

class MongoPipeline1(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(MONGO_URI)

    def to_mongo(self,item):
        collection_name = MONGO_TABLE
        db = self.conn[MONGO_DATABASE]
        # db.authenticate("username", "password")
        db[collection_name].insert(dict(item))
        # db[collection_name].update(dict(item))

    def from_mongo(self):
        collection_name = MONGO_TABLE
        db = self.conn[MONGO_DATABASE]
        # db.authenticate("username", "password")
        collection = db.get_collection(collection_name)
        document = collection.find()
        return document

    def close_mongo(self):
        self.conn.close()

