#-*-coding:utf-8-*-

import os
import xlrd
import pymysql
import redis
from BaiduSpider.settings import *
"""
读取xls文件,存入数据库

"""
# def Reids(keys):
#     _r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWD,db=3)
#     for x in keys:
#         _r.set(x,0)
#
# def Mysql(list):
#     connect = pymysql.Connection(host='127.0.0.1', user='root', password="123456",                                   database='seo')
#     cursor = connect.cursor()
#     for x in list:
#         sql = 'insert into keyword(word) values("{}")'.format(x)
#         cursor.execute(sql)
#     cursor.close()
#     connect.close()


from pymysqlpool import ConnectionPool
import pandas as pd
config = {
'pool_name': 'test',
 'host': 'localhost',
 'port': 3306,
 'user': 'root',
 'password': '123456',
 'database': 'test'
}
def connection_pool():
    pool = ConnectionPool(**config)
    pool.connect()
    return pool
with connection_pool().connection() as conn:
 pd.read_sql('SELECT * FROM user', conn)
# 或者
connection = connection_pool().borrow_connection()
pd.read_sql('SELECT * FROM user', conn)
connection_pool().return_connection(connection)

if __name__ == '__main__':

    res = os.path.realpath('test.xls')
    # workbook = xlrd.open_workbook('C:/Users/管理员/Desktop/project/BaiduSpider/test/test.xls')
    # sheet1 = workbook.sheet_by_index(1)
    # sheet1 = workbook.sheet_by_name('Sheet1')
    # print(sheet1.name,sheet1.nrows,sheet1.ncols)
    # rows = sheet1.col_values(0)
    # # print(rows)
    # # Mysql(rows)
    #
    # Reids(rows)

import requests

