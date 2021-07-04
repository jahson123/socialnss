import random, string
import conn

mycursor = conn.mydb.cursor()


def admin_create(uname, pwd):
    aid_generator = string.ascii_letters + string.digits
    admin_id = ''.join(random.choice(aid_generator) for i in range(7))
    sql = "Insert into admin (AdminID, AdminUname, AdminName, AdminPassword) values (%s, %s, %s, %s)"
    val = (admin_id, uname, "", pwd)
    try:
        mycursor.execute(sql, val)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql, val)
        conn.mydb.commit()
    return uname, pwd


def admin_check(uname, pwd):
    sql = "Select AdminID, AdminUname, AdminPassword from admin where AdminUname='{}' and AdminPassword='{}'".format(uname, pwd)
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admin = mycursor.fetchall()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admin = mycursor.fetchall()
    for check in admin:
        if check[1] == uname and check[2] == pwd:
            session['adminid'] = check[0]
            return 'Success'
    else:
        return flash("Password or Username are wrong")


def admin_name(id):
    sql = "Select AdminName from admin where AdminID='" + id + "'"
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admin = mycursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admin = mycursor.fetchone()
    return admin


def admin_del(id):
    sql = "Delete from admin where AdminID='{}'".format(id)
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()


def admin_select(id):
    sql = "Select * from admin where AdminID='" + id + "'"
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admin = mycursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admin = mycursor.fetchone()
    return admin


def admin_updates(pwd, aid):
    sql = "Update admin set AdminPassword='{}' where AdminID='{}'".format(pwd, aid)
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()
    return 'Update'


def admins_all(aid):
    sql = "Select * from admin where AdminID !='" + aid + "'"
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admins = mycursor.fetchall()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        admins = mycursor.fetchall()
    return admins


def admins_self_update(name, aid):
    sql = "Update admin set AdminName='" + name + "' where AdminID='" + aid + "'"
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()


