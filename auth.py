from flask import request, session, flash
import conn
import uprofile

mycursor = conn.mydb.cursor()


def login():
    if request.method == "POST":
        username = request.form.get('uname')
        pwd = request.form.get('pwd')
        sql = "Select UserID, Username, UserPassword from user where Email_verified='Verified'"
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            user = mycursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            user = mycursor.fetchall()
        for check in user:
            if check[1] == username and check[2] == pwd:
                session['userid'] = check[0]
                uprofile.username(check[0])
                return "Success"
        else:
            return flash("Password or Username are wrong")


def email_verified(uid):
    sql = "Update user set Email_verified='Verified' where UserID= '" + uid + "'"
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()
    return None


def fetch_userid(uname):
    sql = "Select UserID, Email from user where UserName='" + uname + "'"
    cursor = conn.mydb.cursor(buffered=True)
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        user = cursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        user = cursor.fetchone()
    return user
