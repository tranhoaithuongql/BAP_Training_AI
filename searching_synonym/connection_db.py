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
        """
        Kết nối
        :return:
        """
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

    def createDatabase(self):
        """
        Tạo database trong mySQL
        """
        try:
            self.get_connected()
            self.cur.execute(f"create database {self.database}")

        except:
            pass

    def createTable(self, sql):
        """
        Tạo bảng trong mySQL
        :param sql:
        :return:
        """
        try:
            self.get_connected()
            self.cur.execute(sql)

        except:
            pass

    def insert(self, sql, *params):
        """
        Thêm dữ liệu vào database
        :param sql: Câu lệnh truy vấn sql
        :param params:Danh sách tham số
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
        Cập nhật dữ liệu vào database
        :param sql: Câu lệnh truy vấn sql
        :param params: Danh sách tham số
        :return:
        """

        try:
            self.get_connected()
            self.cur.execute(sql, params)
            self.conn.commit()
        except:
            pass

    def delete(self, sql, *params):
        """
        Xóa dữ liệu trong database
        :param sql: Câu lệnh truy vấn sql
        :param params: Danh sách tham số
        :return:
        """
        self.get_connected()
        self.cur.execute(sql, params)
        self.conn.commit()

    def select_word(self):
        """
        Truy vấn dữ liệu từ database
        :return:
        """
        try:
            result = ()
            self.get_connected()
            self.cur.execute("SELECT * FROM word \n")
            result = self.cur.fetchall()
            # for x in result:
            #     print(x)
        except:
            pass
        return result
    def close(self):
        """
        Đóng kết nối
        :return:
        """
        self.conn = None
        self.cur = None

helper = DBHelper('127.0.0.1', 'root', '1234', '3306', 'baitap')



#test insert function

# f = open('3000words.txt', 'r')
# list1 = f.read()
# list1 = list1.split()
# sql = "insert into word(entry_word) values (%s)"
# for i in list1:
#     helper.insert(sql, i)
#
# print('done')