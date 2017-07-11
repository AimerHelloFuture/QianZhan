#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import xlwt


def importData(username, password, database, tablename, datapath):
    '''
    :param username: username of mysql database
    :param password: password of username
    :param database: a database
    :param datapath: the datapath of data folder
    :return: no
    '''

    '''
    step0: connect
    '''
    try:
        conn = mysql.connector.connect(user=username, password=password, database=database, use_unicode=True)
    except mysql.connector.errors.ProgrammingError as e:
        print e
        return -1

    cursor = conn.cursor()

    # cursor.scroll(0, mode='absolute')

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_' + tablename, cell_overwrite_ok=True)

    recu2excel(cursor, sheet, parent='', level=1)

    '''
    fields = cursor.description

    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])

    for row in range(1, len(results) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row-1][col])
    '''

    workbook.save(datapath)

    conn.commit()

    cursor.close()
    conn.close()


number = 1


def recu2excel(cursor, sheet, parent, level):
    sql = 'select * from ' + tablename + ' where binary parent = \'%s\' ' % parent
    cursor.execute(sql)
    results = cursor.fetchall()
    # print len(results)
    sheet.write(0, level - 1, 'name%d' % level)
    if len(results) != 0:
        # sheet.write(0, level-1, 'name'+level)
        for result in range(0, len(results)):
            print results[result][3]
            # print results[result][1]
            print level
            # print len(results)
            global number
            sheet.write(number, level - 1, u'%s' % results[result][3])
            sheet.write(number, 7, u'%s' % results[result][1])
            sheet.write(number, 8, u'%s' % results[result][4])
            number = number + 1
            recu2excel(cursor, sheet, results[result][1], level + 1)
    else:
        # sheet.write(number, level - 1, u'%s' % results[result][3])
        return


if __name__ == '__main__':

    username = 'root'
    password = ''
    database = 'qianzhan'
    tablename = 'qianzhan2'
    datapath = r'D:\YCC\DayTask\Day005\qianzhan.xls'
    importData(username, password, database, tablename, datapath)

