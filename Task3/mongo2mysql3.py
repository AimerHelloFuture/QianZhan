#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import mysql.connector
import requests
import urllib
import threading
import socket
import sys
import csv
import pymongo
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

# --------------------------数据库启动函数------------------------------
def start_MySQL():
    try:
        conn = mysql.connector.connect(user = 'root', password = '', database = 'qianzhan', use_unicode = True)
    except mysql.connector.errors.ProgrammingError as e:
        print e

    cursor = conn.cursor()
    myConn_list = [conn, cursor]
    return myConn_list


# --------------------------关闭数据库--------------------------------
def close_MySQL(conn, cursor):
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    client = pymongo.MongoClient('localhost', 27017)
    qianzhan = client['qianzhan']
    home_info = qianzhan['home_info5']

    myConn_list = start_MySQL()
    conn = myConn_list[0]
    cursor = myConn_list[1]

    table_name = 'qianzhan5'
    ncols = 4
    col_names = []

    for collect in home_info.find():
        try:
            col_names.append('指标名称')
            col_names.append(collect['seque_name'])
            col_names.append(collect['time_name'])
            col_names.append(collect['danwei_name'].replace('：', '').replace('/', '每').replace('=', '等于'))
        except:
            pass

    sql1 = 'delete from ' + table_name
    sql2 = 'truncate ' + table_name
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
    except mysql.connector.errors.ProgrammingError as e:
        print e

    for i in range(1, ncols):
        col_names[2] = col_names[2] + '或' + col_names[i*4 + 2]
        col_names[3] = col_names[3] + '或' + col_names[i*4 + 3]

    sql_create = 'create table if not exists ' \
          + table_name + ' (' + ' id int NOT NULL AUTO_INCREMENT PRIMARY KEY, '

    for i in range(0, ncols):
        sql_create = sql_create + col_names[i] + ' varchar(150)'
        if i != ncols - 1:
            sql_create += ','
    sql_create = sql_create + ')'

    try:
        cursor.execute(sql_create)
    except mysql.connector.errors.ProgrammingError as e:
        print e

    sql_insert = 'insert into ' + table_name + ' values (\'null\', %s, %s, %s, %s)'
    for collect in home_info.find():
        try:
            for num in range(0, len(collect['seque'])):
                cursor.execute(sql_insert, (collect['quota_name'], collect['seque'][num], collect['time'][num], collect['danwei'][num]))
                # print collect['data_name'][num]
        except:
            pass
    # sql2 = 'truncate qianzhan'
    # sql3 = 'delete from qianzhan'
    # cursor.execute(sql)
    # cursor.execute(sql2)
    # cursor.execute(sql3)
    close_MySQL(conn, cursor)
