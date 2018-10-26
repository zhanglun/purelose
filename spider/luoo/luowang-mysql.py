#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-07 04:24:53
# Project: luoo-mysql

from pyspider.libs.base_handler import *
import re
import pymysql.cursors


# connection = pymysql.connect(
#     host='127.0.0.1',
#     port=3306,
#     user='root',
#     db='music'
# )
#
# cursor = connection.cursor()


class DBHelper:
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            db='music',
            use_unicode=True,
            charset="utf8"
        )
        self.table_vol = 'vol'
        self.table_track = 'track'
        self.cursor = self.connection.cursor()

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        finally:
            self.connection.close()

    def insert(self, table, tdict):
        column = ''
        value = ''

        for key in tdict:
            if tdict[key] is not None:
                column += "," + key
                value += "\",\"" + tdict[key]

        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (table, column, value)

        print(sql)

        try:
            self.cursor.execute(sql)
            self.connection.commit()

            last_id = self.cursor.lastrowid

            print(last_id)

            return last_id
        finally:
            self.connection.close()

    def update(self, table, condition, tdict):
        column = ''
        value = ''
        for key in condition:
            column += ",%s=\"%s\"" % (key, condition[key])

        for key in tdict:
            value += ", %s=\"%s\"" % (key, tdict[key])

        column = column[1:]
        value = value[1:]

        sql = 'UPDATE %s SET %s WHERE %s' % (table, value, column)

        print(sql)

        self.execute_sql(sql)

    def save_or_update(self, table, tdict):
        column = ''
        value = ''
        update = ''
        for key in tdict:
            if tdict[key] is not None:
                column += "," + key
                value += "\",\"" + tdict[key]
                update += "," + key + "=\"" + tdict[key] + "\""

        column = column[1:]
        value = value[2:] + "\""
        update = update[1:]

        sql = 'INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s' % (table, column, value, update)

        print(sql)

        self.cursor.execute(sql)
        self.connection.commit()

        last_id = self.cursor.lastrowid

        # self.cursor.close()

    def batch_save_or_update(self, table, tlist):
        columns = []
        values = []
        updates = []

        for tdict in tlist:
            column = ''
            value = ''
            update = ''

            for key in tdict:
                if tdict[key] is not None:
                    column += "," + key
                    value += "\",\"" + tdict[key]
                    update += "," + key + "=VALUES(" + key + ")"

            columns.append("(" + column[1:] + ")")
            values.append("(" + value[2:] + "\"" + ")")
            updates.append(update[1:])

        print(updates)

        sql = 'INSERT INTO %s %s VALUES %s ON DUPLICATE KEY UPDATE %s' % (table, columns[0], ",".join(values),
                                                                          updates[0])

        print(sql)

        self.cursor.execute(sql)
        self.connection.commit()

        last_id = self.cursor.lastrowid

        # self.cursor.close()

db_helper = DBHelper()

data = dict(
    vol_id='123',
    vol_number='123',
    url='123',
    title='123',
    description='changed',
    cover='cover changed',
    vol_prev='123',
    vol_next='23',
)


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
        'itag': 'v0.1.1',
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
        vol_id = response.doc('.btn-action-like').attr['data-id']
        vol_number = response.doc('.vol-number').text()
        tags = []
        track_list = []

        for each in response.doc('.vol-tags').find('.vol-tag-item').items():
            tags.append(each.text())

        for each in response.doc('.track-item').items():
            order_and_name = re.search(r"^(\d+)\.(.+)", each.find('.trackname').text())

            track = {
                'track_id': each.attr.id.replace('track', ''),
                'vol_id': vol_id,
                'order_id': str(int(order_and_name.group(1))),
                'name': re.escape(order_and_name.group(2)),
                'artist': re.escape(each.find('.player-wrapper > .artist').text().replace('Artist:', '').strip()),
                'album': re.escape(each.find('.player-wrapper > .album').text().replace('Album:', '').strip()),
                'cover': each.find('.player-wrapper > .cover').attr.src,
                'url': TRACK_URL_PREFIX + str(vol_number) + '/' + order_and_name.group(1) + '.mp3'
            }


            track_list.append(track)

        db_helper.batch_save_or_update(db_helper.table_track, track_list)

        track_list_id = []

        # track_id 存入 list
        for track in track_list:
            track_list_id.append(str(track['track_id']))

        track_list_id = ",".join(track_list_id)

        result = {
            'vol_id': vol_id,
            'vol_number': vol_number,
            'url': response.url,
            'title': re.escape(response.doc('title').text()),
            'description': re.escape(response.doc('.vol-desc').html().strip()),
            'cover': response.doc('.vol-cover').attr.src,
            'vol_prev': response.doc('.nav-prev').attr.href,
            'vol_next': response.doc('.nav-next').attr.href,
            'created_at': response.doc('.vol-date').html().strip(),
            'track_list_id': track_list_id,
            'tags': re.escape(",".join(tags)),
        }

        db_helper.save_or_update(db_helper.table_vol, result)

        return result

    @catch_status_code_error
    def callback(self, response):
        # if response
        print(response)
        pass




