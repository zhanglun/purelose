#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-09-15 10:27:31
# Project: lianjia_ershoufang_hz

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
        self.table_lianjia_ershoufang = 'lianjia_ershoufang'
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

    __city = 'bj'
    __start_page = 'https://{city}.lianjia.com/ershoufang/'.format(city=__city)

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.__start_page, callback=self.get_areas)

    @config(age=10 * 24 * 60 * 60)
    def get_areas(self, response):
        # 获取筛选项的链接
        area = response.doc('* > * > .m-filter > .position > * > dd > * > div > a').items()

        for each in area:
            print('areas', each.text())
            self.crawl(each.attr.href, callback=self.get_index_list)

        links = response.doc('a[href*="ershoufang"]'.format(city=self.__city)).items()
        reg = re.compile('/ershoufang/\d+.html')

        for link in links:
            print(link.attr.href)
            match = reg.search(link.attr.href)

            if match:
                print('页面连接')
                self.crawl(link.attr.href, callback=self.detail_page)
            elif re.match(r'/ershoufang/([a-zA-z0-9]+/)+', link.attr.href):
                print('正常的index 连接', link.attr.href)
                self.crawl(link.attr.href, callback=self.get_index_list)

    @config(age=10 * 24 * 60 * 60)
    def get_index_list(self, response):
        area = response.doc('* > * > .m-filter > .position > * > dd > * > div > a').items()

        for each in area:
            self.crawl(each.attr.href, callback=self.get_index_list)

        # 详情页面
        items = response.doc('.sellListContent > li.clear.LOGCLICKDATA > .info.clear > .title > a').items()

        for each in items:
            self.crawl(each.attr.href, callback=self.detail_page)

        # 列表页检查分页信息
        page_data = response.doc('.page-box.house-lst-page-box').attr('page-data')

        print('page_data', page_data)

        if page_data:
            page_data = json.loads(page_data)
            total = page_data['totalPage']

            print(re.search('(/pg\d+/$)', response.url))

            # 如果当前url已经是分页访问，不处理
            if re.search('(/pg\d+/$)', response.url) is None:
                for each in range(total):
                    self.crawl(response.url + 'pg' + str(each + 1), callback=self.get_index_list)

    @config(priority=2)
    def detail_page(self, response):
        city = re.search('https://([a-z]+).', response.url).group(1)
        info_block = response.doc('html > body > .sellDetailHeader > div > div > .btnContainer')

        hid = info_block.attr['data-lj_action_resblock_id']
        rid = info_block.attr['data-lj_action_housedel_id']

        transaction_info = response.doc('.transaction li').items()
        transaction = []

        for each in transaction_info:
            label = each.find('.label').text()
            value = each.find('span').eq(1).text()
            transaction.append(dict({
                'label': label,
                'value': value,
            }))

        price = response.doc('.overview .content .price')
        price_total = price.find('.total').text()
        price_total_unit = price.find('.unit').text()
        unit_price = price.find('.unitPriceValue').text()
        community_name = response.doc('.overview > .content > .aroundInfo > .communityName > .info').text()
        area_name = response.doc('.overview > .content > .aroundInfo > .areaName > .info').text()

        # 直接爬接口
        # url = '{API_PREFIX}?hid={hid}&rid={rid}'.format(API_PREFIX=API_PREFIX, hid=hid, rid=rid)
        # self.crawl(url, callback=self.detail_api)
        result = {
            'origin_url': response.url,
            'title': response.doc('title').text(),
            'hid': hid,
            'rid': rid,
            'price_total': price_total,
            'price_total_unit': price_total_unit,
            'unit_price': re.search('(\d*)', unit_price).group(1),
            'community_name': community_name,
            'area_name': area_name,
            'city': city,
            'transaction': json.dumps(transaction, ensure_ascii=False),
            'input_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        }

        db_helper.save_or_update(db_helper.table_lianjia_ershoufang, result)

        # TODO: 针对城市差异化
        if city == 'bj':

            # 获取首付、月供等信息
            cost_url = 'https://{city}.lianjia.com/tools/calccost?house_code={hid}'.format(city=self.__city, hid=hid)

            self.crawl(cost_url, callback=self.get_cast_detail, save={ 'hid': hid})

        return result

    @config(priority=2)
    def get_cast_detail(self, response):
        # hid = re.search('\?house_code=(.+)', response.url).group(1)
        hid = response.save['hid']
        result = response.json
        payment = result['data']['payment']
        cost_payment = {
            'cost_house': payment['cost_house'],
            'cost_jingjiren': payment['cost_jingjiren'],
            'cost_tax': payment['cost_tax'],
        }
        resource = {
            'hid': hid,
            'cost_payment': json.dumps(cost_payment, ensure_ascii=False)
        }

        print(resource)

        db_helper.save_or_update(db_helper.table_lianjia_ershoufang, resource)

        return {
            "url": response.url,
            "resource": resource,
        }

    @catch_status_code_error
    def callback(self, response):
        # if response
        print(response)
        pass




