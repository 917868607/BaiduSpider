# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import xlwt
import datetime
from twisted.enterprise import adbapi
import pymysql
from pymysql import cursors

class BaiduspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class XLSspiderPipeline(object):
    time = datetime.datetime.now().strftime("%Y-%m-%d")

    def __init__(self):
        self.workbook = xlwt.Workbook(encoding="utf-8")
        self.sheet = self.workbook.add_sheet('test',cell_overwrite_ok=True)
        self.sheet.write(0, 0, '端口')
        self.sheet.write(0, 1, '关键字')
        self.sheet.write(0, 2, '平台')
        self.sheet.write(0, 3, '标题')
        self.sheet.write(0, 4, '链接')
        self.sheet.write(0, 5, '时间')
        self.sheet.write(0, 6, '类型')
        self.sheet.write(0, 7, '内容')
        self.sheet.write(0, 8, '备注')
        self.sheet.write(0, 9, '1')
        self.sheet.write(0, 10, '2')
        self.count = 1
    def process_item(self,item,spider):
        self.sheet.write(self.count,0,item['elasticsearch'])
        self.sheet.write(self.count,1,item['key'])
        self.sheet.write(self.count,2,item['comefrom'])
        self.sheet.write(self.count,3,item['title'])
        self.sheet.write(self.count,4,item['link'])
        self.sheet.write(self.count,5,self.time)
        self.sheet.write(self.count,6,item['type'])
        self.sheet.write(self.count,7,item['content'])
        res = '第{}页:{}名'.format(item['page'],item['index'])
        self.sheet.write(self.count,8,res)
        self.count += 1
        return item
    def close_spider(self,spider):
        self.workbook.save('elasticsearch.xls')

class MysqlSpiderPipeline(object):
    def __init__(self,db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls,settings):
        db_params = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PAWD'],
            port = settings['MYSQL_PORT'],
            db = settings['MYSQL_DB'],
            charset = settings['MYSQL_CHARSET'],
            use_unicode = True,
            cursorclass = cursors.DictCursor)
        db_pool = adbapi.ConnectionPool('pymysql',**db_params)
        return cls(db_pool)
    def process_item(self,item,spider):
        query = self.db_pool.runInteraction(self.insert_item,item)
        # query.addErrback(self.handle_error,item,spider)
        return item
    def handle_error(self, failure, item, spider):
        # 输出错误原因
        print(failure)
    def insert_item(self,cursor,item):
        item.insert_mysql(cursor)