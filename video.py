import os
import random
import string

import pyrebase
from flask import request

import conn
import post_content
from date_calc import date_cal

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


mycursor = conn.mydb.cursor(buffered=True)
id_generator = string.ascii_letters + string.digits


class Video:
    def __init__(self, video_name, file):
        self.video_id = 'V_' + ''.join(random.choice(id_generator) for i in range(6))


        self.video_name = video_name
        self.video_type = video_name.split(".")
        self.file = file

        storage = pb.storage()
        path_on_cloud = "video/" + video_name
        storage.child(path_on_cloud).put(file)
        self.video_url = storage.child("video/" + video_name).get_url(None)

        file.seek(0, os.SEEK_END)
        if file.tell() / 1024 >= (1024 * 1024):
            byte = file.tell() / 1024 * 1024
            self.video_size = str(round(byte, 2)) + ' MB'
        else:
            byte = file.tell() / 1024
            self.video_size = str(round(byte, 2)) + ' KB'

    def video_create(self):
        sql = "Insert into video (VideoID, Video_name, Video_url, Video_size, Video_type) values (%s, %s, %s, %s, %s)"
        val = (self.video_id, self.video_name, self.video_url, self.video_size, self.video_type[-1])
        mycursor.execute(sql, val)
        conn.mydb.commit()
        return self.video_id

    def video_id(self):
        mycursor.execute("Select * from video")
        myresult = mycursor.fetchall()
        return myresult[0]

    def method_request(self):
        if request.method == "POST":
            vid = Video.video_create(self)
            return vid

    def update(self, cid):
        sql = "Update video set Video_name='{}', Video_url='{}', Video_size='{}', Video_type='{}'" \
              "where" \
              " VideoID = (SELECT VideoID from post_video WHERE CID='{}')".format(self.video_name, self.video_url, self.video_size, self.video_type[-1], cid)
        mycursor.execute(sql)
        conn.mydb.commit()
        return 'Video update success'

class Post_video:
    def __init__(self, content_id, video_id):
        self.pv_id = 'PV_' + ''.join(random.choice(id_generator) for i in range(6))
        self.content_id = content_id
        self.video_id = video_id

    def create(self):
        sql = "Insert into post_video (PostID_v, VideoID, CID) values (%s, %s, %s)"
        val = (self.pv_id, self.video_id, self.content_id)
        mycursor.execute(sql, val)
        conn.mydb.commit()

    def delete(self):
        sql = "DELETE FROM post_video where PostID_v='{}'".format(self)
        mycursor.execute(sql)
        conn.mydb.commit()
        pass

    def update(self):
        sql = "Update post_video set VideoID='{}' where CID='{}'".format(self.video_id, self.content_id)
        mycursor.execute(sql)
        conn.mydb.commit()

    def fetchall_other(self):
        mycursor.execute("Select  pc.CID, pc.Post_type, v.Video_url, pc.Description, "
                         "up.Name, pc.Post_datetime, pc.UserID, up.profile_pic \
                         from post_content as pc \
                            left join post_video as pv on pc.CID = pv.CID \
                            left join video as v on pv.VideoID = v.VideoID \
                            left join userprofile as up on pc.UserID = up.UserID \
                        where "
                         "pc.Post_status = 'Active' and "
                         "pc.UserID !='{}'  and "
                         "pc.Post_type='Video'".format(self))
        myresult = mycursor.fetchall()
        return myresult

    def fetchall_user(self):
        mycursor.execute("Select  pc.CID, pc.Post_type, v.Video_url, pc.UserID \
                         from post_content as pc \
                            left join post_video as pv on pc.CID = pv.CID \
                            left join video as v on pv.VideoID = v.VideoID \
                        where "
                         "pc.Post_status = 'Active' and "
                         "pc.UserID ='" + self + "'  and "
                         "pc.Post_type='Video'")
        myresult = mycursor.fetchall()
        conn.mydb.commit()
        return myresult

    def fetchone(self, userid):
        mycursor.execute("Select Distinct pc.CID, pc.Post_type, v.Video_url, pc.Description, "
                         "up.Name, pc.Post_datetime, pc.UserID, up.profile_pic \
                          from post_content as pc \
                            left join post_video as pv on pc.CID = pv.CID \
                            left join video as v on pv.VideoID = v.VideoID \
                            left join userprofile as up on pc.UserID = up.UserID \
                          where "
                         "pc.CID = '{}'".format(self))
        x = list(mycursor.fetchone())
        x.append(post_content.Post_content.post_num(self, userid))
        x[5] = date_cal(x[5])
        myresult = tuple(x)
        conn.mydb.commit()
        return myresult

    def method_request(self):
        if request.method == "POST":
            Post_video.create(self)
            return 'Create Success'
"""
def video_update(file, video_name, vid):
    storage = pb.storage()
    path_on_cloud = "video/" + video_name
    storage.child(path_on_cloud).put(file)
    video_url = storage.child("video/" + video_name).get_url(None)
    mimetype = video_name.split(".")

    file.seek(0, os.SEEK_END)
    byte = file.tell() / 1024
    video_size = str(round(byte, 2)) + ' KB'

    sql = "Update video set  \
           Video_name='" + video_name + "', \
           Video_url='" + video_url + "',\
           Video_size='" + video_size + "', \
           Video_type='" + mimetype[-1] + "' where VideoID='" + vid + "'"
    mycursor.execute(sql)
    conn.mydb.commit()

def post_video_update(desc, pvid):
    sql = "Update post_video set Description='" + desc + "' where PostID_v='" + pvid + "'"
    mycursor.execute(sql)
    conn.mydb.commit()


"""






