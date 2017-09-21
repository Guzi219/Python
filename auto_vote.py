# -*- coding: utf-8 -*-
import random
import threading
import time
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class auto_vote:
    def __init__(self):
        self.url = 'http://h5-zb.leju.com/api/v1/plugins/fuelrod/h5/thumbsUp'
        self.ids = ['15500000060935',
                    '15500000051191',
                    '15500000076017',
                    '15500000094706',
                    '15500000077326',
                    '15500000062292',
                    '15500000063152',
                    '15500000031177']


    def main_process(self, topicId):
        # print id
        reqdata = {'liveId': topicId}
        # 定义请求头
        reqheaders = {'Content-type': 'application/x-www-form-urlencoded',
                      'Accept': 'application/json',
                      'Host': 'h5-zb.leju.com',
                      'X-Requested-With': 'XMLHttpRequest',
                      'Origin': 'http://h5-zb.leju.com',
                      'Referer': 'http://zhichang.renren.com',
                      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',}
        #'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36', }
        time.sleep(random.random())

        while True:
            nowTime =  time.ctime()
            r = requests.post(self.url, data=reqdata, headers=reqheaders)
            msg =  '====' + topicId +'===='
            tmpDict = r.json()
            if ('errorMsg' in tmpDict):
                errMsg = tmpDict['errorMsg']
                print (nowTime + msg + errMsg)
            if ('result' in tmpDict):
                print (nowTime + msg + str(tmpDict['result']))

            time.sleep(60.33);


    def main(self):
        threads = []
        for x in range(len(self.ids)):
            t = threading.Thread(target=self.main_process, args=(self.ids[x],))
            threads.append(t)
        for t in threads:
            t.start()
#入口
av = auto_vote()
av.main()

