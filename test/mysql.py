
import pymysql
from DBUtils.PooledDB import PooledDB

DB_TEST_HOST="127.0.0.1"
DB_TEST_PORT=3306
DB_TEST_DBNAME="seo"
DB_TEST_USER="root"
DB_TEST_PASSWORD="123456"


#数据库连接编码
DB_CHARSET="utf8"

#mincached : 启动时开启的闲置连接数量(缺省值 0 以为着开始时不创建连接)
DB_MIN_CACHED=10

#maxcached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
DB_MAX_CACHED=10

#maxshared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
DB_MAX_SHARED=20

#maxconnecyions : 创建连接池的最大数量(缺省值 0 代表不限制)
DB_MAX_CONNECYIONS=100

#blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误<toMany......>; 其他代表阻塞直到连接数减少,连接被分配)
DB_BLOCKING=True

#maxusage : 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
DB_MAX_USAGE=0

#setsession : 一个可选的SQL命令列表用于准备每个会话，如["set datestyle to german", ...]
DB_SET_SESSION=None

'''
@功能：PT数据库连接池
'''
class PTConnectionPool(object):
    __pool = None
    def __enter__(self):
        self.conn = self.getConn()
        self.cursor = self.conn.cursor()
        print("PT数据库创建con和cursor")
        return self

    def getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=DB_MIN_CACHED , maxcached=DB_MAX_CACHED,
                                   maxshared=DB_MAX_SHARED, maxconnections=DB_MAX_CONNECYIONS,
                                   blocking=DB_BLOCKING, maxusage=DB_MAX_USAGE,
                                   setsession=DB_SET_SESSION,
                                   host=DB_TEST_HOST , port=DB_TEST_PORT ,
                                   user=DB_TEST_USER , passwd=DB_TEST_PASSWORD ,
                                   db=DB_TEST_DBNAME , use_unicode=False, charset=DB_CHARSET)
        return self.__pool.connection()

    """
    @summary: 释放连接池资源
    """
    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()
        print("PT连接池释放con和cursor")
'''
@功能：获取PT数据库连接
'''
def getPTConnection():
    return PTConnectionPool()

def TestMySQL():
    #申请资源
    with getPTConnection() as db:
        # SQL 查询语句;
        sql = "SELECT * FROM mess201808"
        try:
            # 获取所有记录列表
            db.cursor.execute(sql)
            results = db.cursor.fetchall()
            for row in results:
                userId = row[0]
                name= row[1]
                sex= row[2]
                createTime = row[3]
                # 打印结果
                print("userId=%d,name=%s,sex=%s,createTime=%s" %(userId, name, sex, createTime ))
        except:
            print("Error: unable to fecth data")
if __name__ == '__main__':

    TestMySQL()