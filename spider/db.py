from pymongo import MongoClient

#
# class DBUtil(object):
#   def __init__(self, dbname=object.dbname):
#     uri = 'mongodb://localhost:27017'
#     # 数据库客户端
#     self.client = MongoClient(uri)
#
#     # 访问数据库
#     self.db = self.client['sitedev']


uri = 'mongodb://localhost:27017'
# 数据库客户端
db_client = MongoClient(uri)

# 访问数据库
db = db_client['sitedev']


# 数据库中的集合
users_collection = db.users
movies_collection = db.movies

print(users_collection.find())

for user in users_collection.find({}):
  print(user)
