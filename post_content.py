import conn
from flask import request
import random, string, datetime
import like, comment, share
import video, photo, share, album
from date_calc import date_cal

mycursor = conn.mydb.cursor(buffered=True)


class Post_content:
    def __init__(self, description, user_id):
        id_generator = string.ascii_letters + string.digits
        self.content_id = 'C_' + "".join(random.choice(id_generator) for i in range(6))
        self.user_id = user_id
        self.description = description

    def create(self):
        files = request.files.getlist("files")
        video_type = ['mp4', 'mov', 'avi', 'webm']
        photo_type = ['gif', 'png', 'jpg', 'jpeg']
        sql = "Insert into post_content (CID, Post_type, Post_status, Description, Post_datetime, UserID)  \
                                    values (%s, %s, %s, %s, %s, %s)"
        if len(files) > 1:
            val = (self.content_id, "Album", "Active", self.description, datetime.datetime.now(), self.user_id)
            try:
                mycursor.execute(sql, val)
                conn.mydb.commit()
            except:
                conn.mydb.ping(True)
                mycursor.execute(sql, val)
                conn.mydb.commit()
            for file in files:
                type = file.filename.split(".")[-1]
                if type in video_type:
                    video_id = video.Video(file.filename, file).method_request()
                    video.Post_video(self.content_id, video_id).method_request()
                elif type in photo_type:
                    photo_id = photo.Photo(file.filename, file).method_request()
                    photo.Post_photo(self.content_id, photo_id).method_request()
        elif len(files) == 1:
            type = files[0].filename.split(".")[-1]
            if type in video_type:
                val = (self.content_id, "Video", "Active", self.description, datetime.datetime.now(), self.user_id)
                try:
                    mycursor.execute(sql, val)
                    conn.mydb.commit()
                except:
                    conn.mydb.ping(True)
                    mycursor.execute(sql, val)
                    conn.mydb.commit()
                video_id = video.Video(files[0].filename, files[0]).method_request()
                video.Post_video(self.content_id, video_id).method_request()
            elif type in photo_type:
                val = (self.content_id, "Photo", "Active", self.description, datetime.datetime.now(), self.user_id)
                try:
                    mycursor.execute(sql, val)
                    conn.mydb.commit()
                except:
                    conn.mydb.ping(True)
                    mycursor.execute(sql, val)
                    conn.mydb.commit()
                photo_id = photo.Photo(files[0].filename, files[0]).method_request()
                photo.Post_photo(self.content_id, photo_id).method_request()
        return self.content_id

    def update(self, types, cid, files):
        sql = "UPDATE `post_content` SET Post_type='{}', Description='{}' where CID='{}'".format(types, self.description, cid)
        try:
            mycursor.execute(sql)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
            conn.mydb.commit()
        if request.args.get("type") == types:
            if types == "Photo":
                photo.Photo(files[0].filename, files[0]).update(cid)
            elif types == "Video":
                video.Video(files[0].filename, files[0]).update(cid)
            elif types == "Album":
                album.album_patch("Photo", files, cid)
                album.album_patch("Video", files, cid)
        elif request.args.get("types") != types:
            if types == "Photo":
                video.Post_video(cid, "").delete()
                photo_id = photo.Photo(files[0].filename, files[0]).method_request()
                photo.Post_photo(cid, photo_id).method_request()
            elif types == "Video":
                photo.Post_photo(cid, "").delete()
                video_id = video.Video(files[0].filename, files[0]).method_request()
                video.Post_video(cid, video_id).method_request()
            elif types == "Album":
                album.album_patch("Photo", files, cid)
                album.album_patch("Video", files, cid)
        return 'Update post content success'

    def delete(self):
        sql = "DELETE FROM post_content where CID='{}'".format(self)
        try:
            mycursor.execute(sql)
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
        conn.mydb.commit()
        pass

    def fetchone(self):
        sql = "Select Distinct * from post_content where CID='{}'".format(self)
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

    def fetchall(self, type):
        sql = "Select * from post_content where post_content.Post_type='{}' Order By post_datetime ".format(type)
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

    def fetchall_other(self):
        """ Fetch share post from share module """
        post = share.fetchall(self)
        """ Fetch album post from album module """
        post += album.album(self)
        """ Fetch all post photo into post """
        for x in video.Post_video.fetchall_other(self):
            a = list(x)
            a.append(Post_content.post_num(a[0], self))
            a[5] = date_cal(a[5])
            b = tuple(a)
            post += [b]
            """ Fetch all post video into post """
        for y in photo.Post_photo.fetchall_other(self):
            a = list(y)
            """ Append post user number for like, share and comment """
            a.append(Post_content.post_num(a[0], self))
            """ Change dateTime into period of date  """
            a[5] = date_cal(a[5])
            b = tuple(a)
            post += [b]
        return post

    def fetchall_user(self):
        """ Fetch all user album into post """
        post = album.album_user(self)
        """ Fetch all post photo into post """
        post += photo.Post_photo.fetchall_user(self)
        """ Fetch all post video into post """
        post += video.Post_video.fetchall_user(self)
        return post

    def method_request(self):
        if request.method == "POST":
            post_create = Post_content.create(self)
            return post_create
        elif request.method == "GET":
            post_view_all = Post_content.view_all(self)
            return post_view_all
        elif request.method == "DELETE":
            Post_content.delete(self)
            pass

    def fetchpost(self, userid):
        if request.args.get("type") == "Photo":
            photos = photo.Post_photo.fetchone(self, userid)
            return photos
        elif request.args.get("type") == "Video":
            videos = video.Post_video.fetchone(self, userid)
            return videos
        elif request.args.get("type") == "Album":
            albums = album.fetchone(self, userid)
            return albums

    def status(self):
        sql = "Select Distinct Post_status from post_content where CID='{}'".format(self)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            status = mycursor.fetchone()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            status = mycursor.fetchone()
        return status[0]


    def post_num(self, userid):
        try:
            num = (like.check_like(self), comment.check_comment(self), share.check_share(self), like.check_user_like(userid, self))
            return num
        except Exception as e:
            return str(e)



