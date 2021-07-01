import pyrebase
import conn
from album import photos, videos

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


def ad_image_one(cid):
    mycursor.execute("Select pc.CID, pc.Description, pc.Post_datetime, pc.Post_status, pc.UserID, "
                     "p.Photo_name, p.Photo_url, p.Photo_size, p.Photo_type, pc.Post_type   \
                      from post_content as pc \
                        left join post_photo as pp on pc.CID = pp.CID \
                        left join photo as p on pp.PhotoID = p.PhotoID \
                      where pc.CID='"+cid+"'")
    myresult = mycursor.fetchone()
    conn.mydb.commit()
    return myresult

def ad_video_one(cid):
    mycursor.execute("Select pc.CID, pc.Description, pc.Post_datetime, pc.Post_status, pc.UserID, "
                     "v.Video_name, v.Video_url, v.Video_size, v.Video_type, pc.Post_type    \
                                  from post_content as pc \
                                  left join post_video as vp on pc.CID = vp.CID \
                                  left join video as v on vp.VideoID = v.VideoID \
                                  where pc.CID='"+cid+"'")
    myresult = mycursor.fetchone()
    conn.mydb.commit()
    return myresult

def ad_share_one(sid):
    sql = "Select * from share where share.ShareID='{}'".format(sid)
    mycursor.execute(sql)
    myresult = mycursor.fetchone()
    return myresult

def ad_album_one(cid):
    """ Fetch specific album """
    mycursor.execute("Select DISTINCT pc.CID, pc.Description, pc.Post_datetime, pc.Post_status, pc.UserID, pc.Post_type \
                      from post_content as pc \
                        left join post_photo as pp on pc.CID = pp.CID \
                        left join userprofile as up on pc.UserID = up.UserID \
                      where "
                     "pc.CID = '{}'".format(cid))
    x = list(mycursor.fetchone())
    myresult = tuple(x)
    url_list = ()
    url_list += tuple(photos(myresult[0]))
    url_list += tuple(videos(myresult[0]))
    add = list(myresult)
    add.insert(2, url_list)
    myresult = tuple(add)
    return myresult

def ad_update_status(status, cid):
    sql = "Update post_content set Post_status='{}' where CID='{}'".format(status, cid)
    mycursor.execute(sql)
    conn.mydb.commit()




