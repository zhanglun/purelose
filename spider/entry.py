#!/user/bin/python

import json
import urllib.request
import upload

from db import DBUtil

data_store = DBUtil({'dbname': 'sitedev'})
movie_collection = data_store.collection.movies
root = 'http://api.douban.com/v2/movie/top250?start=160'


def fetch_json():
    response = urllib.request.urlopen(root)
    data = response.read()  # type: bytes
    string = str(data, encoding='utf-8')  # type: string
    data_dict = json.loads(string)  # dict
    # TODO: 遍历 dict 取出 Object 存入 数据库
    subjects = data_dict['subjects']
    save_json(subjects)


def save_json(data):
    for movie in data:
        # 保存图片到七牛云 尝试
        movie_collection.update_one({'title': movie['title']}, {'$set': movie}, True)

    print('saved.....')
    return data


def start():
    fetch_json()
    return 2

start()
