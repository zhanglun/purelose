#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-07 04:24:53
# Project: luoo-mysql

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
            db='music'
        )
        self.table = 'vol'
        self.cursor = self.connection.cursor()

    def execute_sql(self, sql):
        try:
            self.cursor.execute(sql)
            self.connection.commit()
        finally:
            self.connection.close()

    def insert_vol(self, data):
        column = ''
        value = ''
        for key in data:
            column += "," + key
            value += "','" + data[key]

        column = column[1:]
        value = value[2:] + "'"

        print(column)
        print(value)

        sql = 'INSERT INTO vol (%s) VALUES (%s)' % (column, value)

        print(sql)

        try:
            self.cursor.execute(sql)
            self.connection.commit()

            last_id = self.cursor.lastrowid

            print(last_id)

            return last_id
        finally:
            self.connection.close()


db_helper = DBHelper()
data = dict(
    vol_id='123',
    vol_number='123',
    url='123',
    title='123',
    description='adfasdfd',
    cover='adfasdf',
    vol_prev='123',
    vol_next='23',
)
db_helper.insert_vol(data)
