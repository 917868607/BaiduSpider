#-*-coding:utf-8-*-
import requests
import json
import time
import redis
import random
from fake_useragent import UserAgent
from BaiduSpider.settings import *

URL = 'http://api.ip.data5u.com/dynamic/get.html?order=617edad74d4575cc12bf340c40f7079a&json=1&sep=3'

class IpList(object):
    def __init__(self):
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
        }
    def check_url(self):
        proxy = self.get_ip()
        try:
            response = requests.get('https://www.baidu.com', headers=self.header, proxies={'http': 'http://' + proxy},timeout=0.1)
            # res = requests.get('http://jsonip.com', headers=self.header, proxies={'http': 'http://' + proxy})
            # resp = json.loads(res)
            # print('ip',resp['ip'])
        except Exception as e:
            proxy = self.check_url()
        else:
            if response.status_code == 200:
                proxy = 'http://' + proxy
                return proxy
            else:
                proxy = self.check_url()
        return proxy
    def get_ip(self):
        response = requests.get(url=URL,headers=self.header)
        if response.status_code == 200:
            resp = json.loads(response.text)
            proxy = resp['data'][0]['ip'] + ':' + str(resp['data'][0]['port'])
            return proxy
        else:
            time.sleep(.5)
            proxy = self.get_ip()
            return proxy

    @classmethod
    def return_proxy(cls):
        proxies = cls().check_url()
        return proxies



class GetProxy(object):

    def __init__(self):
        if REDIS_PASSWD:
            pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWD)
        else:
            pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
        self._r = redis.Redis(connection_pool=pool)
    def getproxy(self):
        proxies = self._r.lrange('proxies', 0, self._r.llen('proxies'))
        res = random.choice(proxies)
        res = bytes.decode(res)
        return res
    def testproxy(self):
        useragent = UserAgent()
        header = {'User-Agent':useragent.random}
        proxy = self.getproxy()
        if not proxy:
            self.getproxy()
        try:
            response = requests.get('https://www.baidu.com',headers=header,proxies={'http':'http://'+proxy},timeout=0.1)
        except Exception as e:
            self.removeproxy(proxy)
            proxy = self.testproxy()
        else:
            if response.status_code == 200:
                proxy = 'http://' + proxy
                return proxy
            else:
                proxy = self.testproxy()
        proxy = 'http://' + proxy
        return proxy

    def removeproxy(self,proxy):
        if 'http' in proxy:
            proxy = proxy.split('//')[-1]
        proxies = self._r.lrange('proxies', 0, self._r.llen('proxies'))

        if proxy.encode('utf-8') in proxies:
            proxies.remove(proxy.encode('utf-8'))


    @classmethod
    def returnproxy(cls):
        proxy = cls().testproxy()
        return proxy

if __name__ == '__main__':
    # res = IpList.return_proxy()
    # print(res)
    str = '36.99.17.52:80'
    res = GetProxy()
    ress = res.removeproxy(str)
    print(ress)