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

target_url = 'http://d.qianzhan.com/xdata/list/xfyyy0yyIxPyywyy2xDxfd.html'
# target_url = 'http://d.qianzhan.com/xdata/list/xCxlxvykxw.html'

all_type = []
all_url = []
all_num = []
strr = 'http://d.qianzhan.com'

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }


def getProxyList(mode):
    ProxyList = []
    url = "http://ip.chinaz.com/"

    if mode == 0:
        print "Error"
        return ProxyList

    if (mode >= 1):
        '''爬取西刺代理'''
        page = requests.get("http://cache.baiducontent.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f72967868b432c8fcd1384642c101a39feaf627f5052dcd20d1016db4c4beb802102311451c68cc9f85dadbd855c5c9f5636676bf0&p=90769a4786cc41ac52fecb2b614789&newp=882a9546dc881ee609be9b7c440d91231610db2151d4d11f6b82c825d7331b001c3bbfb423241100d2c3796304a44e5feef43175330025a3dda5c91d9fb4c57479c3787d21&user=baidu&fm=sc&query=%CE%F7%B4%CC%B4%FA%C0%ED&qid=d4f590d500012d17&p1=1&fast=y")
        soup = BeautifulSoup(page.text, 'html5lib')
        trList = soup.find_all('tr')
        for tr in trList:
            tdList = tr.find_all('td')
            if len(tdList)==0:
                continue
            if tdList[5].string.lower()=='http' or tdList[5].string.lower()=='https':
                proxy = {tdList[5].string.lower(): tdList[1].string + ':' + tdList[2].string, }
                try:
                    requests.get(url, proxies=proxy, timeout=0.2)
                except Exception, e:
                    pass
                else:
                    ProxyList.append(proxy)
                    # for _proxy in proxy:
                        # print "%s://%s" % (_proxy, proxy[_proxy])
        # print u'西刺代理爬取结束'

    if (mode==2):
        time.sleep(1)

        '''爬取快代理'''
        page = requests.get("http://www.kuaidaili.com/free/inha/")
        soup = BeautifulSoup(page.text, 'html5lib')
        trList = soup.find_all('tr')
        for tr in trList:
            tdList = tr.find_all('td')
            if(len(tdList)==0):
                continue
            proxy = {tdList[3].string.lower(): tdList[0].string + ':' + tdList[1].string, }
            try:
                requests.get(url, proxies=proxy, timeout=0.2)
            except Exception, e:
                pass
            else:
                ProxyList.append(proxy)
                for _proxy in proxy:
                    print "%s://%s" % (_proxy, proxy[_proxy])
        time.sleep(1)
        page = requests.get("http://www.kuaidaili.com/free/intr/")
        soup = BeautifulSoup(page.text, 'html5lib')
        trList = soup.find_all('tr')
        for tr in trList:
            tdList = tr.find_all('td')
            if(len(tdList)==0):
                continue
            proxy = {tdList[3].string.lower(): tdList[0].string + ':' + tdList[1].string, }
            try:
                requests.get(url, proxies=proxy, timeout=0.2)
            except Exception, e:
                pass
            else:
                ProxyList.append(proxy)
                for _proxy in proxy:
                    print "%s://%s" % (_proxy, proxy[_proxy])
        print u'快代理爬取结束'

    return ProxyList


def use_daili(url):

    for ii in proxieslist:
        try:
            # html = requests.get(url, proxies=ii)
            html = requests.get(url, headers=headers, proxies=ii)
            # tml = requests.get(url, headers=headers)
            return html
        except Exception, e:
            continue


def Get_ip(url, name, parent, child, level):

    html = use_daili(url)
    soup = BeautifulSoup(html.text, 'lxml')
    trs = soup.find_all('div', class_="searchfilter_sub")
    data = {
        'data_url': '', 'data_name': '', 'data_number': '', 'parent': '', 'child': []
    }
    data['data_url'] = url
    data['data_name'] = name
    num = soup.find('div', class_='search-result-tit').find_all('em')[2].text.strip()
    data['data_number'] = num
    data['parent'] = parent
    tr = trs[level - 1]
    tds = tr.find_all('a')
    if level == len(trs) - 1:
        for tdss in tds[1:]:
            child_url = strr + tdss.get('href')
            child.append(child_url)
    data['child'] = child
    print url, name, num, parent, child
    home_info2.insert(data)
    temp = []
    if level == len(trs) - 1:
        for tdss in tds[1:]:
            Get_ip(strr + tdss.get('href'), tdss.text.strip(), url, temp, level + 1)
    else:
        return


if __name__ == '__main__':

    client = pymongo.MongoClient('localhost', 27017)
    qianzhan = client['qianzhan']
    home_info2 = qianzhan['home_info2']
    proxieslist = getProxyList(1)
    Get_ip(target_url, name='中国宏观', parent='', child=[], level=1)
    # t = save_csv(aim_ip)
    # counts = t.Save_ip()

