import conn
import random, string

mycursor = conn.mydb.cursor(buffered=True)

def check_pwd(uid):
    sql = "Select UserPassword from user where UserID='" + uid + "'"
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        user = mycursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        user = mycursor.fetchone()
    return user[0]


def change_pwd(npwd, uid):
    sql = "Update user set UserPassword='" + npwd + "'  where UserID='" + uid + "'"
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()


def reset_pwd(uid, pwd):
    change_pwd(pwd, uid)
    pass
