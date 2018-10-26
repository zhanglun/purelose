#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-07 04:24:53
# Project: luoo

from pyspider.libs.base_handler import *
import re
from pymongo import MongoClient


class DBUtil:
    def __init__(self, object):
        uri = 'mongodb://localhost:27017'

        # 数据库客户端
        self.client = MongoClient(uri)

        # 访问数据库
        self.collection = self.client[object['dbname']]

data_store = DBUtil({'dbname': 'sitedev'})
luoo_collection = data_store.collection.luoo

TRACK_URL_PREFIX = 'http://mp3-cdn2.luoo.net/low/luoo/radio'

HOST = 'www.luoo.net'
REFERER = 'http://www.luoo.net'
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'
HTTP_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': HOST,
    'Referer': REFERER,
    'User-Agent': USER_AGENT,
}


class Handler(BaseHandler):
    retry_delay = {
        0: 12 * 60 * 60,
        '': 24 * 60 * 60
    }
    crawl_config = {
        'headers': {
            'User-Agent': USER_AGENT,
        },
        'auto_crawl': True,
        'itag': 'v0.1.0',
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://www.luoo.net/tag/?p=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        # 详情页面
        for each in response.doc('a[href^="http://www.luoo.net/vol/index/"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        for each in response.doc('a[href^="http://www.luoo.net/tag/?p="]').items():
            self.crawl(each.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        vol_id = int(response.doc('.btn-action-like').attr['data-id'])
        vol_number = int(response.doc('.vol-number').text())
        tags = []
        track_list = []

        for each in response.doc('.vol-tags').find('.vol-tag-item').items():
            tags.append(each.text())

        for each in response.doc('.track-item').items():
            order_and_name = re.search(r"^(\d+)\.(.+)", each.find('.trackname').text(), )
            track_list.append({
                'track_id': each.attr.id.replace('track', ''),
                'vol_id': vol_id,
                'order': order_and_name.group(1),
                'name': order_and_name.group(2),
                'artist': each.find('.player-wrapper > .artist').text().replace('Artist:', '').strip(),
                'album': each.find('.player-wrapper > .album').text().replace('Album:', '').strip(),
                'cover': each.find('.player-wrapper > .cover').attr.src,
                'url': TRACK_URL_PREFIX + str(vol_number) + '/' + order_and_name.group(1) + '.mp3',

            })

        result = {
            'vol_id': vol_id,
            'vol_number': vol_number,
            'url': response.url,
            'title': response.doc('title').text(),
            'desc': response.doc('.vol-desc').html(),
            'cover': response.doc('.vol-cover').attr.src,
            'prev': response.doc('.nav-prev').attr.href,
            'next': response.doc('.nav-next').attr.href,
            'tracks': track_list,
            'tags': tags,
        }

        luoo_collection.update_one({
            'vol_id': result['vol_id']
        }, {
            '$set': result
        }, True)

        return result

    @catch_status_code_error
    def callback(self, response):
        # if response
        print(response)
        pass
