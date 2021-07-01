from flask import request, session, flash
import mysql.connector
import uprofile


mydb = mysql.connector.connect(host="localhost", user="root", password="", database="snss")
mycursor = mydb.cursor()


def login():
    if request.method == "POST":
        username = request.form.get('uname')
        pwd = request.form.get('pwd')
        sql = "Select UserID, Username, UserPassword from user where Email_verified='Verified'"
        mycursor.execute(sql)
        user = mycursor.fetchall()
        mydb.commit()
        for check in user:
            if check[1] == username and check[2] == pwd:
                session['userid'] = check[0]
                uprofile.username(check[0])
                return "Success"
        else:
            return flash("Password or Username are wrong")

def email_verified(uid):
    sql = "Update user set Email_verified='Verified' where UserID= '" + uid + "'"
    mycursor.execute(sql)
    mydb.commit()
    return None

def fetch_userid(uname):
    sql = "Select UserID, Email from user where UserName='" + uname + "'"
    cursor = mydb.cursor(buffered=True)
    cursor.execute(sql)
    user = cursor.fetchone()
    return user
