import conn
import random, string

mycursor = conn.mydb.cursor(buffered=True)

def check_pwd(uid):
    sql = "Select UserPassword from user where UserID='" + uid + "'"
    mycursor.execute(sql)
    user = mycursor.fetchone()
    return user[0]


def change_pwd(npwd, uid):
    sql = "Update user set UserPassword='" + npwd + "'  where UserID='" + uid + "'"
    mycursor.execute(sql)
    conn.mydb.commit()


def reset_pwd(uid):
    pwd_generator = string.ascii_letters + string.digits
    pwd = ''.join(random.choice(pwd_generator) for i in range(10))
    change_pwd(pwd, uid)
    pass
