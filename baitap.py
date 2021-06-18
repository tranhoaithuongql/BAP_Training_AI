
from mysql import connector

class DBHelper():
    def __init__(self, host, user, password, port, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    def connectMysql(self):
        connect = connector.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    port=self.port
                                   )
        return connect


    def connectDatabase(self):
        try:
            connect = connector.connect(host=self.host,
                                        user=self.user,
                                        password=self.password,
                                        port=self.port,
                                        database = self.database
                                        )
            return connect
        except:
            pass

    def createDatabase(self):

        try:
            conn = self.connectMysql()
            cur = conn.cursor()
            cur.execute(f"create database {self.database}")
            cur.close()
            conn.close()
        except:
            pass

    def createTable(self, sql):
        try:
            conn = self.connectDatabase()
            cur = conn.cursor()
            cur.execute(sql)
            cur.close()
            conn.close()
        except:
            pass

    def insert(self,sql, *params):
        """

        :param sql:
        :param params:
        :return:
        """
        try:
            conn = self.connectDatabase()
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            cur.close()
            conn.close()
        except:
            pass

    def update(self, sql, *params):
        """

        :param sql:
        :param params:
        :return:
        """
        try:
            conn = self.connectDatabase()
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            cur.close()
            conn.close()
        except:
            pass

    def delete(self, sql, *params):
        conn = self.connectDatabase()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        cur.close()
        conn.close()


helper = DBHelper('192.168.11.178','root', '1234','3306','testdatabase')

helper.connectMysql()
helper.connectDatabase()

sql="create table testtable1(id int primary key auto_increment,name varchar(50),url varchar(200))"
helper.createTable(sql)

sql = "insert into testtable(name,url) values(%s,%s)"
params = ("thuong", "DT")
helper.insert(sql, *params)

sql = "update testtable set name=%s,url=%s where id=%s"
params = ("noo ha", "nick", "2")
helper.update(sql, *params)

sql="delete from testtable where id=%s"
params=("5")
helper.delete(sql,*params)

print("ok")







