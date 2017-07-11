#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import random
import pymongo
import time
import Queue
import threading
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

Thread_id = 1
Thread_num = 2  # 所开线程数

target_url = Queue.Queue(4)

# 向资源池里面放4个网址用作测试
target_url.put('http://d.qianzhan.com/xdata/details/e4a66419e8453e3d.html')
target_url.put('http://d.qianzhan.com/xdata/details/3bd71dbbf7711d45.html')
target_url.put('http://d.qianzhan.com/xdata/details/99646965fdb23a77.html')
target_url.put('http://d.qianzhan.com/xdata/details/70f0bc98fbbf4243.html')


class proxyListGet():
    def __init__(self, mode):
        self.mode = mode

    def get_proxyList(self):
        ProxyList = []
        url = "http://ip.chinaz.com/"

        if self.mode == 0:
            print "Error"
            return ProxyList

        if (self.mode >= 1):
            '''爬取西刺代理'''
            page = requests.get(
                "http://cache.baiducontent.com/c?m=9f65cb4a8c8507ed4fece763105392230e54f72967868b432c8fcd1384642c101a39feaf627f5052dcd20d1016db4c4beb802102311451c68cc9f85dadbd855c5c9f5636676bf0&p=90769a4786cc41ac52fecb2b614789&newp=882a9546dc881ee609be9b7c440d91231610db2151d4d11f6b82c825d7331b001c3bbfb423241100d2c3796304a44e5feef43175330025a3dda5c91d9fb4c57479c3787d21&user=baidu&fm=sc&query=%CE%F7%B4%CC%B4%FA%C0%ED&qid=d4f590d500012d17&p1=1&fast=y")
            soup = BeautifulSoup(page.text, 'html5lib')
            trList = soup.find_all('tr')
            for tr in trList:
                tdList = tr.find_all('td')
                if len(tdList) == 0:
                    continue
                if tdList[5].string.lower() == 'http' or tdList[5].string.lower() == 'https':
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

        if (self.mode == 2):
            time.sleep(1)

            '''爬取快代理'''
            page = requests.get("http://www.kuaidaili.com/free/inha/")
            soup = BeautifulSoup(page.text, 'html5lib')
            trList = soup.find_all('tr')
            for tr in trList:
                tdList = tr.find_all('td')
                if (len(tdList) == 0):
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
                if (len(tdList) == 0):
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


class proxyUse():
    def __init__(self, url, proxieslist):
        self.url = url
        self.proxieslist = proxieslist

    def use_proxy(self):
        for ii in self.proxieslist:
            try:
                # html = requests.get(url, proxies=ii)
                html = session.get(self.url, headers=headers, proxies=ii)
                # tml = requests.get(url, headers=headers)
                return html
            except Exception, e:
                continue


class infoGet():
    def __init__(self, html):
        self.html = html

    def get_info(self):
        soup = BeautifulSoup(self.html.text, 'lxml')
        data = {
            'quota_name': '', 'seque_name': '', 'time_name': '', 'danwei_name': '', 'seque': [], 'time': [],
            'danwei': []
        }

        quota_name = soup.find('head').find('title').text.strip()
        data['quota_name'] = quota_name[:-12]
        trs = soup.find('table', class_='search-result_table').find_all('tr')
        data['seque_name'] = trs[0].find_all('th')[0].find_all('b')[0].text.strip()
        data['time_name'] = trs[0].find_all('th')[1].find_all('b')[0].text.strip()
        data['danwei_name'] = trs[0].find_all('th')[2].find_all('b')[0].text.strip()
        # print data['seque_name'], data['time_name'], data['danwei_name']
        # print trs[40].find_all('td')[2].find_all('a')
        # print trs[3].find_all('td')[2].find_all('a')
        for index in range(2, len(trs)):
            data['seque'].append(trs[index].find_all('td')[0].text.strip())
            data['time'].append(trs[index].find_all('td')[1].text.strip())
            if trs[index].find_all('td')[2].find_all('a'):  # 判断是否为空list
                data['danwei'].append(trs[index].find_all('td')[2].find_all('a')[0].text.strip())
            else:
                data['danwei'].append(trs[index].find_all('td')[2].text.strip())
                # print data['seque'], data['time'], data['danwei']

        home_info5.insert(data)


class myThread(threading.Thread):

    def __init__(self, q):
        global Thread_id
        threading.Thread.__init__(self)
        self.q = q
        self.Thread_id = Thread_id
        Thread_id = Thread_id + 1

    def run(self):
        while True:
            try:
                task = self.q.get(block=True, timeout=1)  # 不设置阻塞的话会一直去尝试获取资源
            except Queue.Empty:
                print 'Thread',  self.Thread_id, 'end'
                break
            # 取到数据，开始处理（依据需求加处理代码）
            print "Starting ", self.Thread_id
            print task
            pro_use = proxyUse(task, proxieslists)
            html = pro_use.use_proxy()
            info_get = infoGet(html)
            info_get.get_info()
            self.q.task_done()
            print "Ending ", self.Thread_id


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "Missing Parameters"
        sys.exit()
    elif len(sys.argv) > 3:
        print "Too Many Parameters"
        sys.exit()
    username = sys.argv[1]
    password = sys.argv[2]
    # username = '15927403933'
    # password = 'i15927403933'

    client = pymongo.MongoClient('localhost', 27017)
    qianzhan = client['qianzhan']
    home_info5 = qianzhan['home_info5']

    rt = str(random.random())
    session = requests.session()
    session.get('http://user.qianzhan.com/account/doLogin?username=%s&userpwd=%s&callback=loginSuccess&rt=%s' % (username, password, rt))

    pro_list = proxyListGet(1)
    proxieslists = pro_list.get_proxyList()

    # 开Thread_num个线程
    for i in range(0, Thread_num):
        worker = myThread(target_url)
        worker.start()
    # 等待所有的队列资源都用完
    target_url.join()
    print "Exiting Main Thread"


