from flask import request
import random, string
import pyrebase
import conn
import os
from date_calc import date_cal
import post_content

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
id_generator = string.ascii_letters + string.digits


class Photo:
    def __init__(self, photo_name, file):
        self.photo_id = 'P_' + ''.join(random.choice(id_generator) for i in range(6))
        self.photo_name = photo_name
        self.photo_type = photo_name.split(".")
        self.file = file

        storage = pb.storage()
        path_on_cloud = "photo/" + self.photo_name
        storage.child(path_on_cloud).put(self.file)
        self.photo_url = storage.child("photo/" + self.photo_name).get_url(None)

        file.seek(0, os.SEEK_END)
        byte = file.tell() / 1024
        self.photo_size = str(round(byte, 2)) + ' KB'

    def photo_create(self):
        sql = "Insert into photo (PhotoID, Photo_name, Photo_url, Photo_size, Photo_type) values (%s, %s, %s, %s, %s)"
        val = (self.photo_id, self.photo_name, self.photo_url, self.photo_size, self.photo_type[-1])
        try:
            mycursor.execute(sql, val)
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql, val)
        conn.mydb.commit()
        return self.photo_id

    def method_request(self):
        if request.method == "POST":
            pid = Photo.photo_create(self)
            return pid

    def update(self, cid):
        sql = "Update photo set Photo_name='{}', Photo_url='{}', Photo_size='{}', Photo_type='{}'" \
              "where" \
              " PhotoID = (SELECT PhotoID from post_photo WHERE CID='{}')".format(self.photo_name, self.photo_url, self.photo_size, self.photo_type[-1], cid)
        try:
            mycursor.execute(sql)
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
        conn.mydb.commit()
        return 'Photo update success'

class Post_photo:
    def __init__(self, content_id, photo_id):
        self.pp_id = 'PP_' + ''.join(random.choice(id_generator) for i in range(6))
        self.content_id = content_id
        self.photo_id = photo_id

    def post_image_create(self):
        sql = "Insert into post_photo (PostID_p, PhotoID, CID) values (%s, %s, %s)"
        val = (self.pp_id, self.photo_id, self.content_id)
        try:
            mycursor.execute(sql, val)
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql, val)
        conn.mydb.commit()

    def delete(self):
        sql = "DELETE FROM post_photo where PostID_p='{}'".format(self)
        try:
            mycursor.execute(sql)
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
        conn.mydb.commit()
        pass

    def update(self):
        sql = "Update post_photo set PhotoID='{}' where CID='{}'".format(self.photo_id, self.content_id)
        try:
            mycursor.execute(sql)
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
        conn.mydb.commit()
        return self.photo_id

    def post_image_view(self):
        sql = "Select pc.CID, pc.Description, pp.PhotoID, photo.Photo_url " \
              "from post_photo as pp " \
              "left join photo on photo.PhotoID = pp.PhotoID " \
              "left join post_content as pc on pc.CID = pp.CID " \
              "where pp.CID='{}'".format(self)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            myresult = mycursor.fetchone()
        return myresult

    def fetchone(self, userid):
        mycursor.execute("Select Distinct pc.CID, pc.Post_type, p.Photo_url,  pc.Description, "
                         "up.Name, pc.Post_datetime, pc.UserID, up.profile_pic \
                          from post_content as pc \
                            left join post_photo as pp on pc.CID = pp.CID \
                            left join photo as p on pp.PhotoID = p.PhotoID \
                            left join userprofile as up on pc.UserID = up.UserID \
                          where "
                         "pc.CID = '{}'".format(self))
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            x = list(mycursor.fetchone())
            x.append(post_content.Post_content.post_num(self, userid))
            x[5] = date_cal(x[5])
            myresult = tuple(x)
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            x = list(mycursor.fetchone())
            x.append(post_content.Post_content.post_num(self, userid))
            x[5] = date_cal(x[5])
            myresult = tuple(x)
        return myresult


    def fetchall_other(self):
        sql = "Select pc.CID, pc.Post_type, p.Photo_url, pc.Description, " \
                         "up.Name, pc.Post_datetime, pc.UserID, up.profile_pic  \
                          from post_content as pc \
                            left join post_photo as pp on pc.CID = pp.CID \
                            left join photo as p on pp.PhotoID = p.PhotoID \
                            left join userprofile as up on pc.UserID = up.UserID \
                          where " \
                         "pc.Post_status = 'Active' and " \
                         "pc.UserID !='{}' and " \
                         "pc.Post_type='Photo'".format(self)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
        return myresult

    def fetchall_user(self):
        sql = "Select pc.CID, pc.Post_type, p.Photo_url, pc.UserID " \
                         "from post_content as pc \
                            left join post_photo as pp on pc.CID = pp.CID \
                            left join photo as p on pp.PhotoID = p.PhotoID \
                          where " \
                         "pc.Post_status = 'Active' and " \
                         "pc.UserID ='{}' and " \
                         "pc.Post_type='Photo'".format(self)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            myresult = mycursor.fetchall()
        return myresult

    def method_request(self):
        if request.method == "POST":
            Post_photo.post_image_create(self)
            return 'Create Success'
        elif request.method == "GET":
            return Post_photo.post_image_view(self)
