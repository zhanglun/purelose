#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-09-15 10:27:31
# Project: lianjia_chengjiao_bj

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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
        self.table_lianjia_chengjiao = 'lianjia_chengjiao'
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
START_PAGE = 'https://bj.lianjia.com/chengjiao/'
API_PREFIX_CAST = 'https://bj.lianjia.com/ershoufang/housestat'
BLOCK_URL = 'https://' + AREA + '.lianjia.com/chengjiao/resblock?'

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
        self.crawl(START_PAGE, callback=self.area_page)

    @config(age=10 * 24 * 60 * 60)
    def area_page(self, response):
        links = response.doc('a[href*="/chengjiao/"]').items()
        reg = re.compile('/chengjiao/\d+[.html]')

        for link in links:

            match = reg.findall(link.attr.href)

            if match:
                self.crawl(link.attr.href, callback=self.detail_page)
            elif re.match(r'https://[a-z]+.lianjia.com/chengjiao/', link.attr.href):
                print(link.attr.href)
                self.crawl(link.attr.href, callback=self.area_page)
            else:
                self.crawl(link.attr.href, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):

        # 详情页面
        for each in response.doc('* > body > .content > .leftContent > .listContent > li > .info > .title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        city = re.search('https://([a-z]+).', response.url).group(1)
        house_title = response.doc('html > body > .house-title')
        hid = house_title.attr['data-lj_action_resblock_id']
        rid = house_title.attr['data-lj_action_housedel_id']

        sign_at = response.doc('html > body > .LOGVIEW > div.wrapper > span').text()
        sign_method = '链家'
        total_price = response.doc('html > body > .wrapper > .overview > .info.fr > * > .dealTotalPrice > i').text()
        unit_price = response.doc('html > body > .wrapper > .overview > .fr > .price > b').text()
        building_info = response.doc(
            'html > body > .houseContentBox > .m-left > #introduction > .introContent > .base > .content > ul > li')

        building_structure = building_info.eq(0).contents()[1]
        building_floor = building_info.eq(1).contents()[1]
        building_size = building_info.eq(2).contents()[1]
        building_meta = building_info.eq(3).contents()[1]
        building_style = building_info.eq(5).contents()[1]
        building_towards = building_info.eq(6).contents()[1]
        building_year = building_info.eq(7).contents()[1]

        origin_title = response.doc('title').text()
        community_name = origin_title.split()[0]
        areas = response.doc('* > * > * > * > div.agent-box > div.myAgent > .name a')

        if areas.eq(0):
            city_area = areas.eq(0).text()
        else:
            city_area = ''

        if areas.eq(1):
            area_name = areas.eq(1).text()
        else:
            area_name = ''

        result = {
            'hid': hid,
            'rid': rid,
            'sign_at': sign_at,
            'sign_method': sign_method,
            'total_price': total_price,
            'unit_price': unit_price,
            'city_area': city_area,
            'area_name': area_name,
            'community_name': community_name,
            'origin_url': response.url,
            'origin_title': response.doc('title').text(),
            'building_structure': building_structure,
            'building_floor': building_floor,
            'building_size': building_size,
            'building_meta': building_meta,
            'building_style': building_style,
            'building_towards': building_towards,
            'building_year': building_year,
            'input_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'city': city,
        }

        print(result)

        db_helper.save_or_update(db_helper.table_lianjia_chengjiao, result)

        # # 获取小区信息
        # request_block_url = '{prefix}hid={hid}&rid={rid}'.format(prefix=BLOCK_URL, hid=hid, rid=rid)

        # self.crawl(request_block_url, callback=self.get_block_detail)

        return result

    # @config(priority=2)
    # def get_block_detail(self, response):
    #     hid = re.search('\?hid=(.+)&rid=(.+)', response.url).group(1)
    #     rid = re.search('\?hid=(.+)&rid=(.+)', response.url).group(2)
    #     result = response.json
    #     res_block = result['data']['resblock']
    #     cost_payment = {
    #         'cost_house': payment['cost_house'],
    #         'cost_jingjiren': payment['cost_jingjiren'],
    #         'cost_tax': payment['cost_tax'],
    #     }
    #     resource = {
    #         'hid': hid,
    #         'cost_payment': json.dumps(cost_payment, ensure_ascii=False)
    #     }

    #     print(resource)

    #     db_helper.save_or_update(db_helper.table_lianjia_ershoufang, resource)

    #     return {
    #         "url": response.url,
    #         "title": response.doc('title').text(),
    #         "resource": resource,
    #     }

    @catch_status_code_error
    def callback(self, response):
        # if response
        print(response)
        pass



