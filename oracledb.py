'''
链接oracle数据库的python包
安装方法pip install cx_Oracle
'''
import cx_Oracle 
'''
python下的一个数据库连接池包
安装方法pip install DBUtils
'''
from DBUtils.PooledDB  import PooledDB
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
class DataBase:
    '''
        这个类(非多线程版本)的作用是使用不包含数据库连接池的方式，直接连接数据库，该类中提供了，对数据库
        操作所需的增删改查方法，以及链接与断开数据库的方法和事务的回滚与提交方法。
    '''
    def __init__(self,):
        self.__version__='1.0.1'
        self.__DBinstance__=None
        self.__rows__=0

    def __del__(self,):
        if self.__DBinstance__!=None:
            self.__close__()

    def connect(self,user,password,dsn,encoding='utf-8'):
        '''
        user: 数据库用户名
        password: 数据库密码
        dsn：Data Source Name (DSN)的PDO命名惯例为：PDO驱动程序的名称，
             后面为一个冒号，再后面是可选的驱动程序连接数据库变量信息，
             如主机名、端口和数据库名。
        encoding: 编码方式，默认utf-8
        '''
        # 使用connect创建一个数据库链接对象
        self.__DBinstance__=cx_Oracle.connect(user=user,password=password,dsn=dsn,encoding=encoding)
    def unpreparemodify(self,sql,dicts=None):
        try:
            cursor = self.__DBinstance__.cursor()
            cursor.execute(sql,dicts)
            rows = cursor.rowcount
            self.__rows__ += rows
        finally:
            cursor.close()
        return rows

    def modify(self,sql,dicts=None):
        '''
        sql:sql语句
        dicts:占位符对应内容
        '''
        try:
            # 使用cursor() 方法创建一个游标对象cursor
            cursor=self.__DBinstance__.cursor()
            # 预编译sql语句

            cursor.prepare(sql)
            # dicts是用来填充占位符的（可用list,dicts,，tuples,也可按位匹配）
            # execute执行sql语句
            if dicts==None:
                cursor.execute()
            else:
                cursor.execute(None,dicts)
            # rowcount返回的是sql语句影响的行数
            rows=cursor.rowcount
            # 记录总的影响行数
            self.__rows__+=rows
        finally:
            # 关闭游标（光标）
            cursor.close()
        # 返回当前语句影响行数
        return rows
    def unprepareselect(self,sql,dicts=None):
        # print(sql)
        # print(dicts)
        try:
            # print(sql)
            # print(dicts)
            cursor = self.__DBinstance__.cursor()
            cursor.execute(sql,dicts)
            rows = cursor.rowcount
            self.__rows__ += rows
            result = cursor.fetchall()
        finally:
            cursor.close()
        return rows,result
    def select(self,sql,dicts=None):
        try:
            cursor=self.__DBinstance__.cursor()
            '''
            cursor.prepare(sql)
            if dicts==None:
                cursor.execute(None)
            else:
                cursor.execute(None,dicts)
            '''
            cursor.execute(sql, dicts)
            # print("执行完毕")
            rows=cursor.rowcount
            self.__rows__+=rows
            # 返回查询结果
            result=cursor.fetchall()
        finally:
            cursor.close()
        return rows,result

    def rollback(self):
        '''
        数据库事务回滚
        '''
        self.__DBinstance__.rollback()

    def commit(self):
        '''
        数据库事务的提交
        '''
        self.__DBinstance__.commit()
    
    def __close__(self):
        '''
        关闭数据库链接
        '''
        self.__DBinstance__.close()

class Pool:
    '''
    数据库连接池类，用于创建，删除，传递空闲连接的数据库连接池
    DataBasePool与Pool类是关联关系，DataBasePool的实现使用到了Pool类
    '''
    def __init__(self):
        self.pool=None
    
    def __del__(self):
        self.__close__()

    def creatpool(self,user,password,dsn,maxconnections=5,mincached=2,maxcached=3,maxshared=0,enconding='utf-8',**kwargs):
        '''
        数据库连接池的创建
        creator: 使用链接数据库的模块（传入链接数据库使用的python包名）
        maxconnections:链接池允许的最大连接数，0与None表示无限
        mincache: 连接池至少创建的空闲链接（初始化时）
        maxcache: 连接池最多空闲的链接
        maxshared: 连接池中最多共享的连接数量，0和None表示全部共享，
                   (以下说法正确性有待考证)
                   ps:其实并
                   没有什么用，因为pymsql和MySQLDB等模块中的threadsafety都
                   为1，所有值无论设置多少，_maxcahed永远为0，所以永远是所有链接共享
        blocking: 链接池中如果没有可用共享连接后，是否阻塞等待，True表示等待，
                  False表示不等待然后报错
        setsession: 开始会话前执行的命令列表
        ping: ping Mysql 服务端，检查服务是否可用
        user: 用户名
        password: 密码
        dsn: Data Source Name (DSN)的PDO命名惯例为：PDO驱动程序的名称，
             后面为一个冒号，再后面是可选的驱动程序连接数据库变量信息，
             如主机名、端口和数据库名。
        encoding: 编码方式默认utf-8
        '''
        self.pool=PooledDB(
            creator = cx_Oracle, #使用链接数据库的模块
            maxconnections = maxconnections,  #连接池允许的最大连接数，0和None表示没有限制
            mincached = mincached, #初始化时，连接池至少创建的空闲的连接，0表示不创建
            maxcached = maxcached, #连接池空闲的最多连接数，0和None表示没有限制
            maxshared = maxshared, #连接池中最多共享的连接数量，0和None表示全部共享，ps:其实并没有什么用，因为pymsql和MySQLDB等模块中的threadsafety都为1，所有值无论设置多少，_maxcahed永远为0，所以永远是所有链接共享
            blocking = True, #链接池中如果没有可用共享连接后，是否阻塞等待，True表示等待，False表示不等待然后报错
            setsession = [],#开始会话前执行的命令列表
            ping = 0,#ping Mysql 服务端，检查服务是否可用
            user = user,
            password = password,
            dsn = dsn,
            encoding=enconding
        )
    
    def __close__(self):
        if self.pool!=None:
            self.pool.close()
    
    def getconnection(self):
        return self.pool.connection()

class DataBasePool:
    '''
    调用Pool类的封装版本，使用DBUtils包，该类提供了数据库基本的增删改查功能和
    链接/断开数据库与链接/断开数据库池的方法，以及事务的回滚与提交
    '''
    def __init__(self):
        self.__version__='1.0.2'
        self.__DBPoolinstance__=None
        self.rowcount=0

    def __del__(self):
        self.close()

    def connect(self,Pool):
        self.__DBPoolinstance__=Pool.getconnection()
    
    def close(self):
        if self.__DBPoolinstance__!=None:
            self.__DBPoolinstance__.close()
    
    def modify(self,sql,dicts=None,ALLOWSQLI=False):
        if ALLOWSQLI==True:
            try:
                cursor=self.__DBPoolinstance__.cursor()
                # print(dicts)
                if dicts!=None:
                    for key,value in dicts.items():
                        # print(key,value)
                        # print(type(key),type(value))
                        if is_number(value)==True:
                            sql=sql.replace(':'+key,value)
                        else:
                            sql=sql.replace(':'+key,"'"+value+"'")
                # print(sql)
                cursor.prepare(sql)
                cursor.execute(None)
                rows=cursor.rowcount
                self.rowcount+=rows
            finally:
                cursor.close()
            return rows
        else:
            try:
                cursor=self.__DBPoolinstance__.cursor()
                cursor.prepare(sql)
                if dicts==None:
                    cursor.execute(None)
                else:
                    cursor.execute(None,dicts)
                rows=cursor.rowcount
                self.rowcount+=rows
            finally:
                cursor.close()
            return rows

    def select(self,sql,dicts=None,ALLOWSQLI=False):
        if ALLOWSQLI==True:
            try:
                cursor=self.__DBPoolinstance__.cursor()
                # print(dicts)
                if dicts!=None:
                    for key,value in dicts.items():
                        # print(key,value)
                        # print(type(key),type(value))
                        if is_number(value):
                            sql=sql.replace(':'+key,value)
                        else:
                            sql=sql.replace(':'+key,"'"+value+"'")
                # print(sql)
                cursor.prepare(sql)
                cursor.execute(None)
                result=cursor.fetchall()
                rows=cursor.rowcount
                self.rowcount+=rows
            finally:
                cursor.close()
            return rows,result
        else:
            try:
                cursor=self.__DBPoolinstance__.cursor()

                cursor.prepare(sql)
                if dicts==None:
                    cursor.execute(None)
                else:
                    cursor.execute(None,dicts)

                #cursor.execute(sql, dicts)
                result=cursor.fetchall()
                rows=cursor.rowcount
                self.rowcount+=rows
            finally:
                cursor.close()
            return rows,result


    def rollback(self):
        self.__DBPoolinstance__.rollback()

    def commit(self):
        self.__DBPoolinstance__.commit()
