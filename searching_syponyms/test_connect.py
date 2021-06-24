from mysql import connector


class DBHelper(object):
    def __init__(self, host, user, password, port, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        self.conn = None
        self.cur = None
        self.get_connected()

    def get_connected(self):
        if not self.conn:
            self.connectMysql()
            if self.conn:
                self.cur = self.conn.cursor()

    def connectMysql(self):
        self.conn = connector.connect(host=self.host,
                                      user=self.user,
                                      password=self.password,
                                      port=self.port,
                                      database=self.database)

    # def connectDatabase(self):
    #     try:
    #         connect = connector.connect(host=self.host,
    #                                     user=self.user,
    #                                     password=self.password,
    #                                     port=self.port,
    #                                     database=self.database
    #                                     )
    #         return connect
    #     except Exception as err:
    #         raise err

    def createDatabase(self):

        try:
            self.get_connected()
            self.cur.execute(f"create database {self.database}")

        except:
            pass

    def createTable(self, sql):
        try:
            self.get_connected()
            self.cur.execute(sql)

        except:
            pass

    def insert(self, sql, *params):
        """

        :param sql:
        :param params:
        :return:
        """
        try:
            #     self.get_connected()
            self.cur.execute(sql, params)
            self.conn.commit()
        except Exception as err:
            print(err)

    def update(self, sql, *params):
        """
        :param sql:
        :param params:
        :return:
        """
        try:
            self.get_connected()
            self.cur.execute(sql, params)
            self.conn.commit()
        except:
            pass

    def delete(self, sql, *params):
        self.get_connected()
        self.cur.execute(sql, params)
        self.conn.commit()

    def select_word(self, params):
        try:
            self.get_connected()
            self.cur.execute("SELECT * FROM word300")
            result = self.cur.fetchall()
            for x in result:
                print(x)
        except:
            pass

    def close(self):
        self.conn = None
        self.cur = None

# helper = DBHelper('127.0.0.1','root', '1234','3306','baitap')
