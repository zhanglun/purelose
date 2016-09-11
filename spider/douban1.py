#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2016-09-10 12:26:05
# Project: douban

from pyspider.libs.base_handler import *
import re
import string
from pymongo import MongoClient


class DBUtil():
    def __init__(self, object):
        uri = 'mongodb://localhost:27017'
        # 数据库客户端
        self.client = MongoClient(uri)

        # 访问数据库
        self.collection = self.client[object['dbname']]


data_store = DBUtil({'dbname': 'sitedev'})
movie_collection = data_store.collection.movies

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,it;q=0.2,zh-TW;q=0.2,ja;q=0.2,ko;q=0.2',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'gr_user_id=8a6f4105-2552-4098-aa82-3fc96d79141f; bid=mqbBT66ghmg; viewed="3719533_26364209_26337663_6124651_26614077_25774755_1003000_26423783_24748670_2303588"; ue="549936800@qq.com"; dbcl2="50284464:cA70TZYrXVA"; ck=9bGu; _ga=GA1.2.990656205.1431506381; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1473499556%2C%22http%3A%2F%2F0.0.0.0%3A5000%2Ftask%2Fdouban%3A21eb1228d748430ee0e8fa7d145f0c7c%22%5D; ap=1; push_noty_num=0; push_doumail_num=0; __utma=30149280.990656205.1431506381.1473497100.1473499556.174; __utmc=30149280; __utmz=30149280.1473497100.173.107.utmcsr=0.0.0.0:5000|utmccn=(referral)|utmcmd=referral|utmcct=/task/douban:21eb1228d748430ee0e8fa7d145f0c7c; __utmv=30149280.5028; __utma=223695111.1978726812.1452928601.1473497100.1473499556.36; __utmc=223695111; __utmz=223695111.1473497100.35.21.utmcsr=0.0.0.0:5000|utmccn=(referral)|utmcmd=referral|utmcct=/task/douban:21eb1228d748430ee0e8fa7d145f0c7c; _pk_id.100001.4cf6=bceeaec9d758d1fe.1452928601.36.1473499651.1473497099.; _vwo_uuid_v2=E80D6DC392B70A178D88F4B07E212B9F|882cde6bf7a1d58e96107aacc0d1634b',
    'Host': 'movie.douban.com',
    'Pragma': 'no-cache',
    'Referer': 'https://movie.douban.com/tag/%E7%BE%8E%E5%9B%BD',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}


class Handler(BaseHandler):
    crawl_config = {
        'headers': headers
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://movie.douban.com/subject/26266072/?from=subject-page', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        link_items = response.doc('#recommendations > div > dl dd > a').items()
        for each in link_items:
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        link_items = response.doc('#recommendations > div > dl dd > a').items()
        for each in link_items:
            self.crawl(each.attr.href, callback=self.detail_page)
        reg = re.compile('\d+')
        rating = response.doc('#interest_sectl > div > div.rating_self.clearfix > strong').text();
        rating = int(''.join(rating.split('.')))
        rating = rating / 10
        if rating > 5.0:
            result = {
                "url": response.url,
                "title": response.doc('#content > h1 > span:nth-child(1)').text(),
                "douban_id": reg.search(response.url).group()
            }
            movie_collection.update_one({'title': result['title']}, {'$set': result}, True)
        else:
            result = False

        return result
