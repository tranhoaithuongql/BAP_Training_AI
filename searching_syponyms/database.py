import time
from mysql import connector

LIMIT_RETRIES = 3


class Database(object):
    def __init__(self, reconnect: bool = True, **kwargs):
        super(Database, self).__init__()
        self.params = kwargs
        self._connection = None
        self._cursor = None
        self.reconnect = reconnect
        self._init_()

    def __create_connection(self, retry_counter: int = 0):
        if not self._connection:
            try:
                self._connection = connector.connect(**self.params)
                retry_counter = 0
                print("Connection successfully")
                return self._connection
            except connector.Error as err:
                if not self.reconnect or retry_counter >= LIMIT_RETRIES:
                    raise err
                else:
                    retry_counter += 1
                    print("Having some error when trying connect database, "
                          "{} times connecting".format(retry_counter))
                    time.sleep(5)
                    self.__create_connection(retry_counter)
            except (Exception, connector.Error) as err:
                raise err

    def __get_cursor(self):
        if not self._cursor:
            if not self._connection:
                self.__create_connection()
            self._cursor = self._connection.cursor()
        return self._cursor

    def __close(self):
        if self._connection:
            if self._cursor:
                self._cursor.close()
            self._connection.close()
            print("MySQL connection is closed!")
        self._cursor = None
        self._connection = None

    def _init_(self):
        self.__create_connection()
        self.__get_cursor()

    def _reset_(self):
        self.__close()
        self.__create_connection()
        self.__get_cursor()

    def reconnection(self):
        self._reset_()

    def _commit(self):
        self._connection.commit()

    def execute(self, query: str, retry_counter: int = 0, values: tuple = None):
        try:
            if values:
                self._cursor.execute(query, values)
            else:
                self._cursor.execute(query)
            retry_counter = 0
        except connector.Error as err:
            if retry_counter > LIMIT_RETRIES:
                print("Retry number had over limit number", err)
            else:
                retry_counter += 1
                print("Having some error when executing query, "
                      "{} times execute query".format(retry_counter))
                time.sleep(1)
                self.execute(query, retry_counter, values)
        except (Exception, connector.Error) as err:
            print("Error occur when execute query into database:", err)

    def executemany(self, query: str, values: [tuple], retry_counter: int = 0):
        try:
            self._cursor.executemany(query, values)
        except connector.Error as err:
            if retry_counter > LIMIT_RETRIES:
                print("Retry number had over limit number", err)
            else:
                retry_counter += 1
                print("Having some error when executing query, "
                      "{} times execute query".format(retry_counter))
                time.sleep(1)
                self.executemany(query=query, values=values, retry_counter=retry_counter)
        except (Exception, connector.Error) as err:
            print("Error occur when execute query into database:", err)

    def fetch_one(self, query: str, need_fields: bool = False):
        self.execute(query=query)
        value = self._cursor.fetchall()
        if need_fields:
            field_names = [i[0] for i in self._cursor.description]
            return value, field_names
        return value

    def fetch_all(self, query: str, need_fields: bool = False):
        self.execute(query=query)
        values = self._cursor.fetchall()
        if need_fields:
            field_names = [i[0] for i in self._cursor.description]
            return values, field_names
        return values

    def insert_one(self, query, value=None):
        if value:
            self.execute(query=query, values=value[0])
        else:
            self.execute(query=query)
        self._commit()

    def insert_list(self, query, values):
        self.executemany(query, values)
        self._commit()

    def delete_list(self, query):
        self.execute(query)
        self._commit()

    def update_one(self, query):
        self.execute(query)
        self._commit()


def main():
    db_test = {
        "host": "127.0.0.1",
        "user": "root",
        "password": "1234",
        "database": "baitap",
        "port": "3306"
    }
    src_db = Database(**db_test)
    print("okoko")


if __name__ == '__main__':
    main()

