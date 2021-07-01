import mysql.connector as mysql_conn
from mysql.connector import errorcode


class MyConnection:
    def __init__(self, db_host, db_user, db_password, db):
        self.host = db_host
        self.user = db_user
        self.password = db_password
        self.database = db

    def get_conn(self):
        try:
            self.conn = mysql_conn.connect(host=self.host,
                                           user=self.user,
                                           password=self.password,
                                           database=self.database,
                                           buffered=True)
            return self.conn
        except mysql_conn.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("This is an error on your Username or Password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            elif err.errno == 2003:
                print("MySQL server not connect")
            else:
                print(err)


connect = MyConnection("localhost", "root", "", "snss")
mydb = connect.get_conn()
