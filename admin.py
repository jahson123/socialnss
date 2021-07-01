from flask import *
import random, string
import conn

mycursor = conn.mydb.cursor()


def admin_create(uname, pwd):
    aid_generator = string.ascii_letters + string.digits
    admin_id = ''.join(random.choice(aid_generator) for i in range(7))
    sql = "Insert into admin (AdminID, AdminUname, AdminName, AdminPassword) values (%s, %s, %s, %s)"
    val = (admin_id, uname, "", pwd)
    mycursor.execute(sql, val)
    conn.mydb.commit()
    return uname, pwd


def admin_check(uname, pwd):
    sql = "Select AdminID, AdminUname, AdminPassword from admin where AdminUname='{}' and AdminPassword='{}'".format(uname, pwd)
    mycursor.execute(sql)
    admin = mycursor.fetchall()
    conn.mydb.commit()
    return admin


def admin_name(id):
    sql = "Select AdminName from admin where AdminID='" + id + "'"
    mycursor.execute(sql)
    admin = mycursor.fetchone()
    conn.mydb.commit()
    return admin


def admin_delete(id):
    sql = "Delete from admin where AdminID='{}'".format(id)
    mycursor.execute(sql)
    conn.mydb.commit()


def admin_select(id):
    sql = "Select * from admin where AdminID='" + id + "'"
    mycursor.execute(sql)
    admin = mycursor.fetchone()
    conn.mydb.commit()
    return admin


def admin_updates(pwd, aid):
    sql = "Update admin set AdminPassword='{}' where AdminID='{}'".format(pwd, aid)
    mycursor.execute(sql)
    conn.mydb.commit()


def admins_all(aid):
    sql = "Select * from admin where AdminID !='" + aid + "'"
    mycursor.execute(sql)
    admins = mycursor.fetchall()
    conn.mydb.commit()
    return admins


def admins_self_update(name, aid):
    sql = "Update admin set AdminName='" + name + "' where AdminID='" + aid + "'"
    mycursor.execute(sql)
    conn.mydb.commit()

