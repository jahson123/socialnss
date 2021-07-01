import conn
import random, string

mycursor = conn.mydb.cursor()


def users_all():
    mycursor = conn.mydb.cursor()
    sql = "Select UserID, Username, UserPassword, Email, Email_verified from user"
    mycursor.execute(sql)
    users = mycursor.fetchall()
    conn.mydb.commit()
    return users


def user_one(id):
    sql = "Select UserID, Username, UserPassword, Email, Email_verified from user where UserID='" +id+ "'"
    mycursor.execute(sql)
    user = mycursor.fetchone()
    return user


def user_create(username, pwd, email):
    uid_generator = string.ascii_letters + string.digits
    user_id = ''.join(random.choice(uid_generator) for i in range(6))
    sql = "Insert into user (UserID, Username, UserPassword, Email, Email_verified) values (%s, %s, %s, %s, %s)"
    val = (user_id, username, pwd, email, 'unverified')
    mycursor.execute(sql, val)
    conn.mydb.commit()
    return user_id


def user_delete(userid):
    sql = "Delete from user where UserID='{}'".format(userid)
    mycursor.execute(sql)
    conn.mydb.commit()


def user_name(userid):
    sql = "Select Name from userprofile where UserID='" + userid + "'"
    mycursor.execute(sql)
    user = mycursor.fetchone()
    return user


def fetchall_user():
    sql = "Select * from user"
    mycursor.execute(sql)
    users = mycursor.fetchall()
    return users
