#-*-coding:utf-8-*-

import re
import time
import json
import pymysql
import redis
import requests
import hashlib
from BaiduSpider.settings import *
from .ip_api import IpList
from urllib import parse
from .mysql_connect import getPTConnection

class Untiles(object):

    @classmethod
    def check_str(cls,string):
        """清洗字符串"""
        pattern = re.compile('【|】| |\n|\r|\t|\xa0|<.*?>|{.*?}|\u3000')
        string = re.sub(pattern,'',string).replace('(sinaads=window.sinaads||[]).push()','')
        if '收起公告重磅组团赚百万车币报名就拿奖' in string or '吉普牧马人换代，为销量放弃越野，国产车的机会来了' in string:
            string = cls().check_china(string)
        return string
    def check_china(self,string):
        res = ''.join(re.findall(re.compile('[\u4e00-\u9fa5]'), string))
        return res

    @classmethod
    def get_url(cls,url):
        """从定向获取url"""
        if 'so.com' in url or 'baidu.com' in url or 'sogou.com' in url:
            if '//m.' in url:
                User = 'Mozilla/5.0 (Linux; Android 4.4.2; OPPO R11 Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36'
            else:
                User = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
            headers = {
                "User-Agent":'{}'.format(User),
                "Accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                "Upgrade-Insecure-Requests": "1"
            }
            try:
                response = requests.get(url=url,allow_redirects=False,headers=headers)
            except Exception as e:
                url = cls.get_url(url)
                return url
            else:
                if response.status_code == 302:
                    try:
                        if not "http" in response.headers['location']:
                            return url
                        return response.headers['location']  # 返回指向的地址
                    except:
                        pass
                else:
                    try :
                        if 'url' in response.text:
                            url = re.search(re.compile('url=(.*?)\"'),response.text).group(1)
                        else:
                            url = re.search(re.compile("URL=(.*?)>"), response.text).group(1).replace("'", '').replace('"', '')
                    except Exception as e:
                    # with open('get_url.html','w',encoding='utf-8') as f:
                    #     f.write(response.text)
                        print(e)
                        return url
        return url


def getMD5(string):
    """获取MD5加密后的数据"""
    h1 = hashlib.md5()
    h1.update(string.encode(encoding='utf-8'))
    str = h1.hexdigest()
    return str


def sendstr(redis_key):
    _res = [eval(bytes.decode(x)) for x in redis_key]
    return _res

def get_comefrom(string,code):
    list1 = re.findall(re.compile('_(\w+)'),string)
    list2 = re.findall(re.compile('-(\w+)'),string)
    list3 = re.findall(re.compile('- (\w+)'),string)
    list4 = re.findall(re.compile('- (\w+)'),string)
    list5 = []
    if '|' in string:
        list5 = re.findall(re.compile('|(\w+)'),string)
        list5 = string.replace('|',',').split(',')
        print(list5)
    if list1:
        """配置"""
        if '_' in ''.join(list1):
            list1 = ''.join(list1).split('_')
            if not list1[-1]:
                list1 = list1[:-1]
        _list = list1[-1]
        if '配置' in ''.join(list1):
            _list = code
    if list2:
        if  '贴吧' in ''.join(list2):
            _list = '百度贴吧'
        elif '玩车' in ''.join(list2):
            _list = code
        else:
            _list = list2[-1]
    if  '优酷' in string:
        _list = '优酷网'
    if list3:
        if '【' in ''.join(list3[-1]):
            _list = ''.join(list3[-1]).replace('【','').replace('】','')
        else:
            _list = list3[-1]
    if list4:
        _list = list4[-1]
    if list5 != []:
        _list = list5[-1]
    if not list4 and  not list1 and not list2:
        _list = code
    return _list


class CheckMysql(object):
    # with getPTConnection() as db
    # def __init__(self):
    #     self.db = getPTConnection()

    def select(self,url):
        with getPTConnection() as db:
            ls = ""
            sql = 'select url from urls'
            db.cursor.execute(sql)
            res = db.cursor.fetchall()
            for x in [z.decode('utf-8') for x in res for z in x]:
                if x in url:
                    print('url{}在过滤器中'.format(url))
                    ls = x
            if ls:
                return True
            else:
                return False

    def get_key(self):
        with getPTConnection() as db:
            sql = 'select word from keyword'
            db.cursor.execute(sql)
            res = db.cursor.fetchall()
            res = list(set([z.decode('utf-8') for x in res for z in x]))
            # self.closeMysql()
            return res

    # def closeMysql(self):
    #     self.cursor.close()
    #     self.connect.close()
class RedisCheck(object):
    def __init__(self):
        if REDIS_PASSWD:
            pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT,password=REDIS_PASSWD)
        else:
            pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_PORT)
        self._r = redis.Redis(connection_pool=pool)
    def return_good_bad(self,content,type='good'):
        goods = ''
        if type == 'good':
            self._r.connection_pool.connection_kwargs['db'] = 3
        else:
            self._r.connection_pool.connection_kwargs['db'] = 2
            # self._r.connection_pool._available_connections[0]._description_args['db'] = 2
        keys = self._r.keys()
        print([x.decode('utf-8') for x in keys])
        for x in [x.decode('utf-8') for x in keys]:
            if x in content:
                goods = x
        if goods:
            return True
        else:
            return False

    def check_url(self,link):
        """过滤url"""
        url = ''
        self._r.connection_pool.connection_kwargs['db'] = 6
        keys = self._r.keys()
        for x in [x.decode('utf-8') for x in keys]:
            if x in link:
                url = x
        if url:
            return True
        else:
            return False
        
    def redis_connect(self,db):
        self._r.connection_pool.connection_kwargs['db'] = db
        return self._r
def get_pull(key,url):
    start_url = 'https://sug.so.360.cn/suggest?callback=suggest_so&encodein=utf-8&encodeout=utf-8&format=json&fields=word&word={}'.format(key)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        "Referer": '{}'.format(url)}
    response = requests.get(url=start_url, allow_redirects=False, headers=headers)
    res = response.content.decode('utf-8')
    res = re.search(re.compile('suggest_so\((.*?)\)'),res).group(1)
    json_res = json.loads(res)

def now_to_timestamp(digits = 10):
    """获取13位时间"""
    time_stamp = time.time()
    digits = 10 ** (digits -10)
    time_stamp = int(round(time_stamp*digits))
    return time_stamp

if __name__ == '__main__':

    # url = 'https://www.so.com/'
    # r = RedisCheck()
    # r.return_good()

    def Reids(keys):
        "6 url 3 goood 2 bad 45"
        _r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWD, db=6)
        for x in keys:
            _r.set(x, 0)
    check = CheckMysql()
    Reids(check.decide_good_bed(key='url',db='urls'))
    # key = '自由光'
    # key = parse.quote(key)
    # get_pull(key,url)
    # string = '自由光|cherokee-1报价_图片_配置_视频_团购_论坛|车讯网...'
    # res = get_comefrom(string,code='123')
    # print(res)
    # url = 'https://www.autohome.com.cn/3872/'
    # check = Checkurl()
    # res = check.get_key()
    # print(res)
#     res = GetProxy()
#     proxy = res.returnproxy()
#     print(proxy)
#
#     url = ' http://www.so.com/link?m=amGj8rD6wGU20X3YXhMnpzFXJvCUI%2B%2BRp6FkcRVnZwUS4MSPy0iMM9M4v2Z2RZNLbt9DOfi8H5timbhPLVyyvP6rUCHHu0NvxwN0X7R9%2BqfXBWZzUd7UGT7KMH1wgDTPv'
#
#     res = Untiles.get_url(url)
#     print(res)