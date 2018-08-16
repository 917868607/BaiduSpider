# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
import redis
import hashlib
from .untils.until import *
from .settings import REDIS_PORT,REDIS_PASSWD,REDIS_HOST,REDIS_DB


class BaiduspiderItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    elasticsearch = scrapy.Field()
    key = scrapy.Field()
    comefrom = scrapy.Field()
    link = scrapy.Field()
    type = scrapy.Field()
    index = scrapy.Field()
    page = scrapy.Field()
    content = scrapy.Field()
    """判断type为0 的 ,size1 = 1 确定为中性"""
    size1 = scrapy.Field()
    """参数"""
    # red = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=5)
    red = RedisCheck().redis_connect(db=5)
    _time = datetime.datetime.now().strftime("%Y%m%d")
    r_time = datetime.datetime.now().strftime("%Y%m")
    time = 'mess' + r_time
    def insert_mysql(self,cursor):
        sql = self.create_mysql()
        cursor.execute(sql)
        print(self.time)
        sql = 'insert into {}(' \
              'elasticsearch,' \
              'key1,' \
              'comefrom,' \
              'title,' \
              'link,' \
              'type,' \
              'time,' \
              'index1,' \
              'page,' \
              'content,' \
              'size1) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'.format(self.time)

        params = (self['elasticsearch'],
              self['key'],
              self['comefrom'],
              self['title'],
              self['link'],
              self['type'],
              self._time,
              int(self['index']),
              int(self['page']),
              self['content'],
              int(self['size1']))
        """key时间 [{'title':标题,'index':第几名,'page':第几页,'type':类型}]"""
        try:
            cursor.execute(sql, params)
        except Exception as e:
            print('错误的参数',params)

        self.red.lpush(self._time + self['elasticsearch'],{self['key']:{'title':self['title'],'index':self['index'],'page':self['page'],"type":self['type'],
                                                                        'size1':self['size1'],'contents':self['content']
                                                                        }})
        self.red.expire(self._time,datetime.timedelta(days=30))
        """redis 去重"""

    def create_mysql(self):
        sql = 'CREATE TABLE IF NOT EXISTS {}(' \
              'id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,' \
              'elasticsearch VARCHAR(50) NOT NULL,' \
              'key1 VARCHAR(250) NOT NULL,' \
              'comefrom VARCHAR(250) NOT NULL,' \
              'title VARCHAR(250) NOT NULL,' \
              'link TEXT NOT NULL,' \
              'type INTEGER NOT NULL,' \
              'time VARCHAR(50) NOT NULL,' \
              'index1 INTEGER NOT NULL,' \
              'page INTEGER NOT NULL,' \
              'content TEXT,' \
              'size1 INTEGER,' \
              'size2 TEXT,size3 TEXT,size4 TEXT,size5 TEXT)'.format(self.time)
        return sql

class BaiduItem(scrapy.Item):
    """相关搜索"""
    elasticsearch = scrapy.Field()
    key = scrapy.Field()
    comefrom = scrapy.Field()
    title = scrapy.Field()
    """相关搜搜情感展示 link (reverse) type(front) """
    link = scrapy.Field()
    type = scrapy.Field()
    # r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
    r = RedisCheck().redis_connect(db=4)
    _time = datetime.datetime.now().strftime("%Y%m%d")
    r_time = datetime.datetime.now().strftime("%Y%m")
    time = 'rele' + r_time
    def insert_mysql(self,cursor):
        sql = self.create_mysql()
        cursor.execute(sql)
        sql = 'insert into {}(elasticsearch,key1,comefrom,title,negative_prob,positive_prob,time) values(%s,%s,%s,%s,%s,%s,%s)'.format(self.time)
        params = (self['elasticsearch'],self['key'],self['comefrom'],self['title'],self['type'],self['link'],self._time)
        """存redis进行去重key 时间 [{'title':标题,'front':type','reverse':link,'time':''}]"""
        key_name = 'rele' + self._time + self['elasticsearch']
        res = self.r.lrange(key_name, 0, self.r.llen(key_name))
        _res = sendstr(res)
        if res == [] or self['title'] not in [val for x in _res for val in x.get('{}'.format(self['key']),{'key':1}).values()]:
            self.r.lpush(
                key_name,
                {self['key']:{'title': self['title'],
                 'negative_prob': self['type'],
                 'positive_prob': self['link'],
                 'time': self._time}})
            self.r.expire(key_name, datetime.timedelta(days=30))

            cursor.execute(sql, params)


    def create_mysql(self):
        sql = 'CREATE TABLE IF NOT EXISTS {}(' \
              'id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,' \
              'elasticsearch VARCHAR(50) NOT NULL,' \
              'key1 VARCHAR(250) NOT NULL,' \
              'comefrom VARCHAR(250) NOT NULL,' \
              'title VARCHAR(250) NOT NULL,' \
              'negative_prob FLOAT NOT NULL,' \
              'positive_prob FLOAT NOT NULL,' \
              'time VARCHAR(50) NOT NULL,' \
              'size1 TEXT,' \
              'size2 TEXT,' \
              'size3 TEXT,' \
              'size4 TEXT,' \
              'size5 TEXT)'.format(self.time)
        return sql

class PullKeyItem(scrapy.Item):
    """下拉搜搜
    key 搜搜关键字
    index 下拉字位置
    type == 正负面
    """
    elasticsearch = scrapy.Field()
    key = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    index = scrapy.Field()
    # r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=4)
    r = RedisCheck().redis_connect(db=4)
    _time = datetime.datetime.now().strftime("%Y%m%d")
    r_time = datetime.datetime.now().strftime("%Y%m")
    time = 'pull' + r_time
    def insert_mysql(self,cursor):
        sql = self.create_mysql()
        cursor.execute(sql)
        sql = 'insert into {}(' \
              'elasticsearch,' \
              'key1,' \
              'title,' \
              'time,negative_prob,positive_prob) values(%s,%s,%s,%s,%s,%s)'.format(self.time)
        params = (
            self['elasticsearch'],
            self['key'],
            self['title'],
            self._time,
            self['type'],
            self['index'])
        """存redis进行去重key 时间 [{'title':标题,'front':','reverse':,'time':''}]"""
        key_name = 'pull' + self._time + self['elasticsearch']
        res = self.r.lrange(key_name, 0, self.r.llen(key_name))
        _res = sendstr(res)
        if res == [] or self['title'] not in [val for x in _res for val in x.get('{}'.format(self['key']),{'key':1}).values()]:
            self.r.lpush(
                key_name,
                {self['key']:{'title': self['title'],
                 'negative_prob': self['type'],
                 'positive_prob': self['index'],
                 'time': self._time}})
            self.r.expire(key_name, datetime.timedelta(days=30))
            cursor.execute(sql, params)
    def create_mysql(self):
        sql = 'CREATE TABLE IF NOT EXISTS {}(' \
              'id integer PRIMARY KEY AUTO_INCREMENT NOT NULL,' \
              'elasticsearch VARCHAR(50) NOT NULL,' \
              'key1 VARCHAR(250) NOT NULL,' \
              'title VARCHAR(250) NOT NULL,' \
              'time VARCHAR(50) NOT NULL,' \
              'negative_prob FLOAT NOT NULL,' \
              'positive_prob FLOAT NOT NULL,' \
              'size1 TEXT,' \
              'size2 TEXT,' \
              'size3 TEXT,' \
              'size4 TEXT,' \
              'size5 TEXT)'.format(self.time)
        return sql