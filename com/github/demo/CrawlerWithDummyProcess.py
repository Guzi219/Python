# -*- coding:utf-8 -*-
import threading
import time
import urllib2
from multiprocessing.dummy import Pool as ThreadPool
from BeautifulSoup import BeautifulSoup

class Fetcher:
    def __init__(self):
        self.opener = urllib2.build_opener(urllib2.HTTPHandler)

    def getContent(self, link):
        try:
            content = self.opener.open(link).read()
            if len(content) > 0:
                html = BeautifulSoup(content)
                titleDiv = html.find('title')
                if len(titleDiv) > 0:
                    print link, titleDiv.text, '\n'
        except Exception, what:
            print link, what

    def getNum(self, link):
        print '\n', threading.current_thread().getName()

    def getCC(self, link):
        print self.opener.open(link).read()


if __name__ == "__main__":
    t0 = time.time()
    links = ['http://www.jfinal.com/project?p=%d' % i for i in range(1, 6)]
    # Make the Pool of workers
    pool = ThreadPool(2)
    # Open the urls in their own threads
    # and return the results
    results = pool.map(Fetcher().getCC, links)
    # close the pool and wait for the work to finish
    pool.close()
    pool.join()

    t1 = time.time()
    print str(t1 - t0)
