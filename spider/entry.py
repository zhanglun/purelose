#!/user/bin/python

import json
import urllib.request
import upload

root = 'http://api.douban.com//v2/movie/top250'


def fetchJSON ():
  response = urllib.request.urlopen(root)
  data = response.read()  # type: bytes
  string = str(data, encoding='utf-8') # type: string
  data_dict = json.loads(string) # dict
  # TODO: 遍历 dict 取出 Object 存入 数据库
  subjects = data_dict['subjects']
  print(subjects)


def start():
  fetchJSON()
  return 2


start()
