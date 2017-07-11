#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading
import time

Thread_id = 1
Thread_num = 1  # 所开线程数


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
            self.q.task_done()
            print "Ending ", self.Thread_id


q = Queue.Queue(2)

# 向资源池里面放2个网址用作测试
q.put('http://d.qianzhan.com/xdata/details/e4a66419e8453e3d.html')
q.put('http://d.qianzhan.com/xdata/details/3bd71dbbf7711d45.html')

# 开Thread_num个线程
for i in range(0, Thread_num):
    worker = myThread(q)
    worker.start()
# 等待所有的队列资源都用完
q.join()
print "Exiting Main Thread"