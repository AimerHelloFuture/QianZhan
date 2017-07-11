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
    home_info3 = qianzhan['home_info3']

    myConn_list = start_MySQL()
    conn = myConn_list[0]
    cursor = myConn_list[1]

    sql = 'insert into qianzhan3 values (\'null\', %s, %s, %s, %s, %s)'
    for collect in home_info3.find():
        try:
            for num in range(0, len(collect['data_url'])):
                cursor.execute(sql, (collect['quota_fenlei'], collect['data_name'][num], collect['data_url'][num], collect['data_danwei'][num],  collect['data_time'][num]))
                # print collect['data_name'][num]
        except:
            pass
    # sql2 = 'truncate qianzhan'
    # sql3 = 'delete from qianzhan'
    # cursor.execute(sql)
    # cursor.execute(sql2)
    # cursor.execute(sql3)
    close_MySQL(conn, cursor)
