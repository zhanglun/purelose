#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-01-07 04:24:53
# Project: luoo-mysql

import pymysql.cursors

connection = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    db='music'
)

cursor = connection.cursor()

print(cursor)

try:

    sql = 'INSERT INTO vol (vol_id, vol_number, url, title, description, cover, vol_prev, vol_next) VALUES (%s, %s, ' \
          '%s, ' \
          '%s, ' \
          '%s, ' \
          '%s, ' \
          '%s, %s)'
    # sql = 'INSERT INTO vol (vol_id) VALUES (%s)'
    cursor.execute(sql, (1, 2, 'adsf', 'adf', 'adf', 'afd', 'adf', 'adf'))
    connection.commit()
finally:
    connection.close()


