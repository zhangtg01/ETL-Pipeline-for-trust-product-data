
import pymysql
import cx_Oracle
# 在oracle设置成中文
import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class DBConn(object):
    def __init__(
            self,
            dbtype='', host='', port='', user='', passwd='', dbname=''
    ):
        self.dbtype = dbtype
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        if dbtype == 'mysql':
            self.db = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd,
                                      db=self.dbname, charset='utf8')
        elif dbtype == 'oracle':
            self.db = cx_Oracle.connect(self.user, self.passwd, self.host + ':' + self.port + '/' + self.dbname)

    # 插入sql
    def bulk_insert_mysql(self, sql, record_list):
        cursor = self.db.cursor()
        cursor.executemany(sql, record_list)
        self.db.commit()
        cursor.close()

    def get_sql(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        return data

    def update_sql(self, sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        self.db.commit()
        cursor.close()