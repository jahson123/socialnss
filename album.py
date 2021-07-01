import pyrebase
import conn
from date_calc import date_cal
import post_content
from photo import Post_photo, Photo
from video import Post_video, Video

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

def photos(cid):
    """ Fetch photo url & name from photo table """
    mycursor.execute("Select p.Photo_url, p.Photo_name from post_photo as pp \
                        inner join photo as p on pp.PhotoID = p.PhotoID \
                        where pp.CID ='{}'".format(cid))
    result = mycursor.fetchall()
    return result


def videos(cid):
    """ Fetch video url & name from photo table """
    mycursor.execute("Select v.Video_url, v.Video_name from post_video as pv \
                        inner join video as v on pv.VideoID = v.VideoID \
                        where pv.CID ='{}'".format(cid))
    result = mycursor.fetchall()
    return result

def album(userid):
    """ Fetch album """
    album = []
    mycursor.execute("Select DISTINCT pc.CID, pc.Post_type, pc.Description, "
                     "up.Name, pc.Post_datetime, pc.UserID, up.profile_pic \
                      from post_content as pc \
                        left join post_photo as pp on pc.CID = pp.CID \
                        left join userprofile as up on pc.UserID = up.UserID \
                      where "
                     "pc.Post_status = 'Active' and "
                     "pc.UserID !='{}' and "
                     "pc.Post_type='Album'".format(userid))
    myresult = mycursor.fetchall()
    for x in range(len(myresult)):
        url_list = ()
        url_list += tuple(photos(myresult[x][0]))
        url_list += tuple(videos(myresult[x][0]))
        add = list(myresult[x])
        add.append(post_content.Post_content.post_num(add[0], userid))
        add[4] = date_cal(add[4])
        add.insert(2, url_list)
        b = tuple(add)
        album += [b]
    return album


def album_user(userid):
    """ Fetch specific user all album """
    album = []
    mycursor.execute("Select DISTINCT pc.CID, pc.Post_type, pc.UserID \
                      from post_content as pc \
                        left join post_photo as pp on pc.CID = pp.CID \
                        left join userprofile as up on pc.UserID = up.UserID \
                      where "
                     "pc.Post_status = 'Active' and "
                     "pc.UserID ='{}' and "
                     "pc.Post_type='Album'".format(userid))
    myresult = mycursor.fetchall()
    conn.mydb.commit()
    for x in myresult:
        url_list = ()
        url_list += tuple(photos(x[0]))
        url_list += tuple(videos(x[0]))
        add = list(x)
        add.insert(2, url_list)
        b = tuple(add)
        album += [b]
    return album

def fetchone(cid, userid):
    """ Fetch specific user post album """
    mycursor.execute("Select DISTINCT pc.CID, pc.Post_type, pc.Description, "
                     "up.Name, pc.Post_datetime, pc.UserID, up.Profile_pic \
                      from post_content as pc \
                        left join post_photo as pp on pc.CID = pp.CID \
                        left join userprofile as up on pc.UserID = up.UserID \
                      where "
                     "pc.CID = '{}'".format(cid))
    x= list(mycursor.fetchone())
    x.append(post_content.Post_content.post_num(cid, userid))
    x[4] = date_cal(x[4])
    myresult = tuple(x)
    url_list = ()
    url_list += tuple(photos(myresult[0]))
    url_list += tuple(videos(myresult[0]))
    add = list(myresult)
    add.insert(2, url_list)
    myresult = tuple(add)
    return myresult

def album_patch(type, files, cid):
    image = []
    video = []
    for i in range(len(files)):
        a = files[i].filename.split(".")[-1]
        if a in ['gif', 'png', 'jpg', 'jpeg']:
            image.append(files[i])
        elif a in ['mp4', 'mov', 'avi', 'webm']:
            video.append(files[i])
    if type == "Photo":
        photo_list = album_select(type, cid)
        if len(image) > len(photo_list):
            for num in range(len(image) - len(photo_list)):
                photo_id = Photo(image[-num-1].filename, image[-num-1]).method_request()
                Post_photo(cid, photo_id).method_request()
            for i in range(len(image) - (len(image) - len(photo_list))):
                photo_list = album_select(type, cid)
                photo_id = Photo(image[i].filename, image[i]).method_request()
                album_update(type, photo_id, "p", photo_list[i][0])
        elif len(photo_list) > len(image):
            for num in range(len(photo_list) - len(image)):
                Post_photo.delete(photo_list[-num-1][0])
            for i in range(len(image)):
                photo_id = Photo(image[i].filename, image[i]).method_request()
                album_update(type, photo_id, "p", photo_list[i][0])
        elif len(image) == len(photo_list):
            for i in range(len(image)):
                photo_id = Photo(image[i].filename, image[i]).method_request()
                album_update(type, photo_id, "p", photo_list[i][0])
                i += 1
        elif len(image) == 0:
            for num in range(len(photo_list)):
                Post_video.delete(photo_list[num][0])
    elif type == "Video":
        video_list = album_select(type, cid)
        if len(video) > len(video_list):
            for num in range(len(video) - len(video_list)):
                video_id = Video(video[-num-1].filename, video[-num-1]).method_request()
                Post_video(cid, video_id).method_request()
            for i in range(len(video) - (len(video) - len(video_list))):
                video_list = album_select(type, cid)
                video_id = Video(video[i].filename, video[i]).method_request()
                album_update(type, video_id, "v", video_list[i][0])
        elif len(video_list) > len(video):
            for num in range(len(video_list) - len(video)):
                Post_video.delete(video_list[-num-1][0])
            for i in range(len(video)):
                video_id = Video(video[i].filename, video[i]).method_request()
                album_update(type, video_id, "v", video_list[i][0])
        elif len(video) == len(video_list):
            for i in range(len(video)):
                video_id = Video(video[i].filename, video[i]).method_request()
                album_update(type, video_id, "v", video_list[i][0])
                i += 1
        elif len(video) == 0:
            for num in range(len(video_list)):
                Post_video.delete(video_list[num][0])
    return "Album patch success"

def album_select(type, cid):
    sql = "Select * from post_{} where CID='{}'".format(type,  cid)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult


def album_update(type, type_id, id, post_id):
    sql = "Update post_{} set {}ID='{}' where PostID_{}='{}'".format(type, type, type_id, id, post_id)
    mycursor.execute(sql)
    conn.mydb.commit()

def content_select(type):
    sql = "Select {}ID from {} ".format(type, type)
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    return myresult
