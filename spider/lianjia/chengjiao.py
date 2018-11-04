#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-09-15 10:27:31
# Project: lianjia_chengjiao_bj

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
            db='lianjia',
            use_unicode=True,
            charset="utf8"
        )
        self.table_lianjia_chengjiao = 'chengjiao'
        self.cursor = self.connection.cursor()

    def execute_sql(self, sql):
        cursor = self.connection.cursors()

        try:
            cursor.execute(sql)
            self.connection.commit()
        finally:
            cursor.close()

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
        cursor = self.connection.cursor()

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

        cursor.execute(sql)

        self.connection.commit()

        last_id = cursor.lastrowid

        cursor.close()

    def batch_save_or_update(self, table, tlist):
        columns = []
        values = []
        updates = []
        cursor = self.connection.cursor()

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

        cursor.execute(sql)
        self.connection.commit()

        last_id = self.cursor.lastrowid

        # self.cursor.close()


db_helper = DBHelper()

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
        'connect_timeout': 50,
        'timeout': 200,
        'auto_crawl': True,
        'itag': 'v0.1.1',
    }

    __city = 'bj'
    __start_page = 'https://{city}.lianjia.com/chengjiao/'.format(city=__city)
    __res_block_url = 'https://{city}.lianjia.com/chengjiao/resblock'.format(city=__city)

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.__start_page, callback=self.get_areas, connect_timeout = 50, timeout = 200)

    @config(age=10 * 24 * 60 * 60)
    def get_areas(self, response):
        area = response.doc('* > * > .m-filter > .position > * > dd > * > div > a').items()

        for each in area:
            self.crawl(each.attr.href, callback=self.get_index_list, connect_timeout = 50, timeout = 200)

        links = response.doc('a[href*="https://{city}.lianjia.com/chengjiao/"]'.format(city=self.__city)).items()
        reg = re.compile('chengjiao/\d+.html$')

        for link in links:
            match = reg.search(link.attr.href)

            # 页面连接
            if match:
                self.crawl(link.attr.href, callback=self.detail_page, connect_timeout = 50, timeout = 200)
            elif re.match(r'/chengjiao/([a-zA-z0-9]+/)+', link.attr.href):
                self.crawl(link.attr.href, callback=self.get_index_list, connect_timeout = 50, timeout = 200)

    @config(age=10 * 24 * 60 * 60)
    def get_index_list(self, response):
        area = response.doc('* > * > .m-filter > .position > * > dd > * > div > a').items()

        for each in area:
            self.crawl(each.attr.href, callback=self.get_index_list, connect_timeout = 50, timeout = 200)

        # 详情页面
        for each in response.doc('* > body > .content > .leftContent > .listContent > li > .info > .title > a').items():
            self.crawl(each.attr.href, callback=self.detail_page, connect_timeout = 50, timeout = 200)

        # 列表页检查分页信息
        page_data = response.doc('.page-box.house-lst-page-box').attr('page-data')

        print('page_data', page_data)

        if page_data:
            page_data = json.loads(page_data)
            total = page_data['totalPage']

            # 如果当前url已经是分页访问，不处理
            if re.search('(/pg\d+/$)', response.url) is None:
                for each in range(total):
                    self.crawl(response.url + 'pg' + str(each + 1), callback=self.get_index_list, connect_timeout = 50, timeout = 200)

    @config(priority=2)
    def detail_page(self, response):
        city = re.search('https://([a-z]+).', response.url).group(1)
        house_title = response.doc('html > body > .house-title')
        hid = house_title.attr['data-lj_action_resblock_id']
        rid = house_title.attr['data-lj_action_housedel_id']

        sign_at = response.doc('html > body > .LOGVIEW > div.wrapper > span').text()
        sign_at_time = re.search('(\d+(\.\d+)?(\.\d+)?)', sign_at);

        if sign_at_time and sign_at_time.group(1):
            value = sign_at_time.group(1) + '.01.01'
            value = '.'.join(value.split('.')[:3])
            print(value)
            sign_at =  time.strftime('%Y-%m-%d', time.strptime(value, '%Y.%m.%d'))

        sign_method = '链家'
        total_price = response.doc('html > body > .wrapper > .overview > .info.fr > * > .dealTotalPrice > i').text()
        unit_price = response.doc('html > body > .wrapper > .overview > .fr > .price > b').text()
        building_info = response.doc(
            'html > body > .houseContentBox > .m-left > #introduction > .introContent > .base > .content > ul > li')

        building_structure = building_info.eq(0).contents()[1].strip()
        building_floor = building_info.eq(1).contents()[1].strip()
        building_size = building_info.eq(2).contents()[1].strip()
        building_meta = building_info.eq(3).contents()[1].strip()
        building_style = building_info.eq(5).contents()[1].strip()
        building_towards = building_info.eq(6).contents()[1].strip()
        building_year = building_info.eq(7).contents()[1].strip()

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

        self.crawl(self.__res_block_url, params={ 'hid': hid, 'rid': rid }, save=result, callback=self.get_res_block_detail, connect_timeout = 50, timeout = 200)

    @config(priority=2)
    def get_res_block_detail(self, response):
        resource = response.save
        data = response.json
        res_block = data['data']

        print(res_block)

        try:
            resource['community_meta'] = json.dumps(res_block)
        except:
            resource['community_meta'] = '';

        print(resource)

        db_helper.save_or_update(db_helper.table_lianjia_chengjiao, resource)

    @catch_status_code_error
    def callback(self, response):
        # if response
        print(response)
        pass



