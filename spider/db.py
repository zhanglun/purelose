from pymongo import MongoClient


class DBUtil():
    def __init__(self, object):
        uri = 'mongodb://localhost:27017'
        # 数据库客户端
        self.client = MongoClient(uri)

        # 访问数据库
        self.collection = self.client[object['dbname']]
