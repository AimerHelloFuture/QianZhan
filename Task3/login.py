#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 单线程登录且抓取数据入mongodb

import requests
import sys
import random
import pymongo
from bs4 import BeautifulSoup


headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }


target_url = 'http://d.qianzhan.com/xdata/details/82e2c790b3c03ba4.html' # 要爬取的指标网址


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
            html = s.get(url, headers=headers, proxies=ii)
            # html = requests.get(url, headers=headers)
            return html
        except Exception, e:
            continue


def get_info(url):
    html = use_daili(url)
    soup = BeautifulSoup(html.text, 'lxml')
    data = {
        'quota_name': '', 'seque_name': '', 'time_name': '', 'danwei_name': '', 'seque': [], 'time': [], 'danwei' : []
    }

    quota_name = soup.find('head').find('title').text.strip()
    data['quota_name'] = quota_name[:-12]
    trs = soup.find('table', class_='search-result_table').find_all('tr')
    print len(trs)
    data['seque_name'] = trs[0].find_all('th')[0].find_all('b')[0].text.strip()
    data['time_name'] = trs[0].find_all('th')[1].find_all('b')[0].text.strip()
    data['danwei_name'] = trs[0].find_all('th')[2].find_all('b')[0].text.strip()
    # print data['seque_name'], data['time_name'], data['danwei_name']
    # print trs[40].find_all('td')[2].find_all('a')
    # print trs[3].find_all('td')[2].find_all('a')
    for index in range(2, len(trs)):
        data['seque'].append(trs[index].find_all('td')[0].text.strip())
        data['time'].append(trs[index].find_all('td')[1].text.strip())
        if trs[index].find_all('td')[2].find_all('a'): # 判断是否为空list
            data['danwei'].append(trs[index].find_all('td')[2].find_all('a')[0].text.strip())
        else:
            data['danwei'].append(trs[index].find_all('td')[2].text.strip())
        # print data['seque'], data['time'], data['danwei']

    home_info4.insert(data)


if __name__ == '__main__':
    # username = sys.argv[1]
    # password = sys.argv[2]

    client = pymongo.MongoClient('localhost', 27017)
    qianzhan = client['qianzhan']
    home_info4 = qianzhan['home_info4']

    username = '15927403933'
    password = 'i15927403933'
    rt = str(random.random())
    proxieslist = getProxyList(1)
    s = requests.session()
    s.get('http://user.qianzhan.com/account/doLogin?username=%s&userpwd=%s&callback=loginSuccess&rt=%s' % (username, password, rt))
    # 测试是否登录
    # r = s.get('http://user.qianzhan.com/profile/4640015.html')
    # soup = BeautifulSoup(r.text, 'lxml')
    # i = soup.select('div.login_af')
    # print i
    get_info(target_url)
    # 测试是否登录
    # r = s.get('http://user.qianzhan.com/profile/4640015.html')
    # soup = BeautifulSoup(r.text, 'lxml')
    # i = soup.select('div.login_af')
    # print i