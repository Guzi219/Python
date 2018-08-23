# -*- coding:utf-8 -*-
import urllib2
from threading import Thread,Lock
from Queue import Queue
import time

from BeautifulSoup import BeautifulSoup


class Fetcher:
    def __init__(self,threads):
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)
        self.lock = Lock() #线程锁
        self.q_req = Queue() #任务队列
        self.q_ans = Queue() #完成队列
        self.threads = threads
        for i in range(threads):
            t = Thread(target=self.threadget)
            t.setDaemon(True)
            t.start()
        self.running = 0

    def __del__(self): #解构时需等待两个队列完成
        time.sleep(0.5)
        self.q_req.join()
        self.q_ans.join()

    def taskleft(self):
        return self.q_req.qsize()+self.q_ans.qsize()+self.running

    def push(self,req):
        self.q_req.put(req)

    def pop(self):
        return self.q_ans.get()

    def threadget(self):
        while True:
            req = self.q_req.get()
            with self.lock: #要保证该操作的原子性，进入critical area
                self.running += 1
            try:
                ans = self.opener.open(req).read()
                # print ans
            except Exception, what:
                ans = ''
                print what
            self.q_ans.put((req,ans))
            with self.lock:
                self.running -= 1
            self.q_req.task_done()
            time.sleep(0.1) # don't spam

if __name__ == "__main__":
    t0 = time.time()
    links = [ 'http://www.verycd.com/topics/%d/'%i for i in range(5430,5460) ]
    f = Fetcher(threads=10)
    for url in links:
        f.push(url)

    while f.taskleft():
        url,content = f.pop()
        if len(content) > 0:
            html = BeautifulSoup(content)
            titleDiv = html.find('title')
            if len(titleDiv) > 0:
                print titleDiv.text

    t1 = time.time()
    print str(t1 - t0)