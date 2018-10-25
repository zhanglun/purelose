#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-09-15 10:27:31
# Project: lianjia_xiaoqu_bj

from pyspider.libs.base_handler import *
import pymysql.cursors
import json
import re
import time


class DBHelper:
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            db='house',
            use_unicode=True,
            charset="utf8"
        )
        self.table_lianjia_xiaoqu = 'lianjia_xiaoqu'
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
                column += ',' + key
                value += '\',\'' + tdict[key]

        column = column[1:]
        value = value[2:] + '\''

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
                column += ',' + key
                value += '\',\'' + tdict[key]
                update += '\',' + key + '=\'' + tdict[key]

        column = column[1:]
        value = value[2:] + '\''
        update = update[2:] + '\''

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

AREA = 'bj'
START_PAGE = 'https://bj.lianjia.com/xiaoqu/'
API_PREFIX_CAST = 'https://bj.lianjia.com/ershoufang/housestat'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36'


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
        self.crawl('https://bj.lianjia.com/xiaoqu/?from=rec', callback=self.index_page)

        for each in range(150):
            # if re.match('/ershoufang/pg\d+', each.attr.href, re.U):
            self.crawl(START_PAGE + 'pg' + str(each), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        # 详情页面
        for each in response.doc('* > body > .content > .leftContent > .listContent > li > .info > .title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        rid = re.search('xiaoqu/([0-9a-zA-Z]+)', response.url).group(1)
        name = response.doc('html > body > * > div.xiaoquDetailHeaderContent > div.detailHeader.fl > .detailTitle').text()
        address = response.doc('html > body > * > div.xiaoquDetailHeaderContent.clear > .detailHeader.fl > .detailDesc').text()
        average_price = response.doc('html > body > .xiaoquOverview > .fr > .xiaoquPrice > div > .xiaoquUnitPrice').text()

        xiaoqu_info = response.doc('html > body > .xiaoquOverview > .fr > .xiaoquInfo > div > .xiaoquInfoContent')

        print(xiaoqu_info)

        building_year = xiaoqu_info.eq(0).text()
        building_type = xiaoqu_info.eq(1).text()
        service_fees = xiaoqu_info.eq(2).text()
        service_company = xiaoqu_info.eq(3).text()
        developers = xiaoqu_info.eq(4).text()
        building_count = xiaoqu_info.eq(5).text()
        house_count = xiaoqu_info.eq(5).text()

        result = {
            'rid': rid,
            'name': name,
            'address': address,
            'origin_url': response.url,
            'origin_title': response.doc('title').text(),
            'average_price': average_price,
            'building_year': building_year,
            'building_type': building_type,
            'building_count': building_count,
            'service_fees': service_fees,
            'service_company': service_company,
            'developers': developers,
            'house_count': house_count,
            'input_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'city': AREA,
        }

        db_helper.save_or_update(db_helper.table_lianjia_xiaoqu, result)

        return result


