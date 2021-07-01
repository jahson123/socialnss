import pyrebase
import conn
from flask import session, request
import os

config = {
  "apiKey": "AIzaSyAci0y2q2vdPlWEscYy9yGBnoT5G6pRfvw",
  "authDomain": "unique-perigee-299514.firebaseapp.com",
  "databaseURL": "https://unique-perigee-299514-default-rtdb.firebaseio.com",
  "projectId": "unique-perigee-299514",
  "storageBucket": "unique-perigee-299514.appspot.com",
  "appId": "1:780859428666:web:186013295f48ab39958a03",
  "measurementId": "G-X85C75VPCY"
}
pb = pyrebase.initialize_app(config)

mycursor = conn.mydb.cursor()


def user_select(uid):
    sql = "Select Username, UserPassword, Email from user where UserID='" + uid + "'"
    mycursor.execute(sql)
    user = mycursor.fetchone()
    conn.mydb.commit()
    return user


def profile_select(uid):
    sql = "Select Distinct * from userprofile where UserID='" + uid + "'"
    mycursor.execute(sql)
    pro = mycursor.fetchone()
    conn.mydb.commit()
    return pro


def profile_update(uid, name, gender, status, dob):
    sql = "Update userprofile set Name='" + name + "', Gender='"+gender+"', Status='"+status+"', Date_of_birth='"+dob+"' where UserID='"+uid+"'"
    mycursor.execute(sql)
    conn.mydb.commit()

def user_update(uid, email):
    sql = "Update user set Email='"+email+"' where UserID='" + uid + "'"
    mycursor.execute(sql)
    conn.mydb.commit()

def user_update_admin(uid, pwd, email, ev):
    sql = "Update user set UserPassword='"+pwd+"', Email='"+email+"', Email_verified='" +ev+ "' where UserID='" + uid + "'"
    mycursor.execute(sql)
    conn.mydb.commit()

def profile_create(uid, name):
    sql = "Insert into userprofile (UserID, Name, Gender, Status, Date_of_birth, Profile_pic) values (%s, %s, %s, %s, %s, %s)"
    val = (uid, name, "None", "None", "", "")
    mycursor.execute(sql, val)
    conn.mydb.commit()

def username(uid):
    sql = "SELECT user.Username, p.Name from user " \
          "join userprofile as p on user.UserID = p.UserID " \
          "where user.UserID='{}'".format(uid)
    mycursor.execute(sql)
    name = mycursor.fetchone()
    session['name'] = name[1]


def profile_photo(uid):
    file = request.files['file']
    storage = pb.storage()
    path_on_cloud = "profile_pic/" + file.filename
    storage.child(path_on_cloud).put(file)
    photo_url = storage.child("profile_pic/" + file.filename).get_url(None)
    file.seek(0, os.SEEK_END)

    sql = "Update userprofile set Profile_pic='{}' where UserID='{}'".format(photo_url, uid)
    mycursor.execute(sql)
    conn.mydb.commit()




