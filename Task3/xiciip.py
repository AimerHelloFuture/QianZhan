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
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

target_url = []
aim_ip = []
for i in range(2, 1700):
    # url = 'http://www.xicidaili.com/nn/%d' % i
    url = 'http://www.kuaidaili.com/free/outha/%d' % i
    target_url.append(url)

all_message = []


class ipGet(threading.Thread):
    def __init__(self, target):
        threading.Thread.__init__(self)
        self.target = target

    def Get_ip(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        html = requests.get(self.target, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        trs = soup.find('div', id='list').find_all('tr')
        for tr in trs[1:]:
            tds = tr.find_all('td')
            ip = tds[0].text.strip()
            opening = tds[1].text.strip()
            message = [ip, opening]
            all_message.append(message)
            print ip, opening

    def run(self):
        self.Get_ip()


class ipCheck(threading.Thread):
    def __init__(self, ipList):
        threading.Thread.__init__(self)
        self.ipList = ipList
        self.timeout = 6
        # self.test_url = 'https://www.jd.com/'
        self.test_url = 'http: // d.qianzhan.com / xdata / list / xfyyy0yyIxPyywyy2xDxfd.html'
        self.another_url = 'https://www.taobao.com/'

    def Check_ip(self):
        socket.setdefaulttimeout(3)
        for ip in self.ipList:
            try:
                proxy_host = "http://" + ip[0] + ":" + ip[1]
                proxy_temp = {"http": proxy_host}
                t_start = time.time()
                res = urllib.urlopen(self.test_url, proxies=proxy_temp).read()
                res2 = urllib.urlopen(self.another_url, proxies=proxy_temp).read()
                t_use = time.time() - t_start
                soup = BeautifulSoup(res, 'lxml')
                soup2 = BeautifulSoup(res2, 'lxml')
                ans = soup.find('link', rel='dns-prefetch')
                ans2 = soup2.find('link', rel='dns-prefetch')
                if ans != None and ans2 != None:
                    aim_ip.append((ip[0], ip[1], t_use))
                else:
                    continue
            except Exception, e:
                print e

    def run(self):
        self.Check_ip()


class save_csv():
    def __init__(self, SaveList):
        self.driver = 'root'
        self.server = ''
        self.database = 'xiciip'
        self.savelist = SaveList

    def Save_ip(self):
        base = mysql.connector.connect(user=self.driver, password=self.server, database=self.database, use_unicode=True)
        # base = mysql.connector.connect('root', '', 'xiciip', use_unicode=True)
        source = base.cursor()
        counts = 0
        for each in self.savelist:
            source.execute("select * from ip where ips='%s'" % each[0])
            if source.fetchone() == None:
                source.execute("Insert into ip values('%s','%s','%s')" % (each[0], each[1], each[2]))
            else:
                print "The ip: '%s' is exist!" % each[0]
                counts += 1
        base.commit()
        source.close()
        base.close()
        return counts


if __name__ == '__main__':
    GetThreading = []
    CheckThreading = []

    for i in range(len(target_url)):
        t = ipGet(target_url[i])
        GetThreading.append(t)
    for i in range(len(GetThreading)):
        GetThreading[i].start()
        print GetThreading[i].is_alive()
    for i in range(len(GetThreading)):
        GetThreading[i].join()




    print '@' * 3 + ' ' * 2 + "总共抓取了%s个代理" % len(all_message) + ' ' * 2 + '@' * 3

    for i in range(20):
        t = ipCheck(all_message[((len(all_message) + 19) / 20) * i:((len(all_message) + 19) / 20) * (i + 1)])
        CheckThreading.append(t)
    for i in range(len(CheckThreading)):
        CheckThreading[i].start()
        # print CheckThreading[i].is_alive()
    for i in range(len(CheckThreading)):
        CheckThreading[i].join()

    print '@' * 3 + ' ' * 2 + "总共有%s个代理通过校验" % len(aim_ip) + ' ' * 2 + '@' * 3

    t = save_csv(aim_ip)
    counts = t.Save_ip()

    print '@' * 3 + ' ' * 2 + "总共新增%s个代理" % (len(aim_ip) - counts) + ' ' * 2 + '@' * 3

