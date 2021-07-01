import random, string
import datetime
from flask import request
import conn
from date_calc import date_cal
import post_content

mycursor = conn.mydb.cursor()


def share(cid, describe, uid):
    if request.method == "POST":
        share_id_generator = string.ascii_letters + string.digits
        share_id = 'S'+''.join(random.choice(share_id_generator) for i in range(5))
        sql = "Insert into share (ShareID, CID, Share_describe, Share_dateTime, UserID, Share_Status) values (%s, %s, %s, %s, %s, %s)"
        val = (share_id, cid, describe, datetime.datetime.now(), uid, "Active")
        try:
            mycursor.execute(sql, val)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql, val)
            conn.mydb.commit()
        return 'Create share success'


def check_share(cid):
    sql = "SELECT count(CID) as NumPostShared from `share` WHERE CID='" + cid + "' "
    cursor = conn.mydb.cursor(buffered=True)
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        num = cursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        num = cursor.fetchone()
    return num[0]


def fetchphoto_others(userid):
    sql = "Select share.ShareID, pc.Post_type, p.Photo_url, pc.Description, " \
                     "up.Name, pc.UserID, share.Share_describe, share.Share_dateTime, up.UserID, up2.Name, " \
                     "up2.Profile_pic, pc.Post_status  \
                     from share \
                        left join post_content as pc on share.CID = pc.CID \
                        left join post_photo as pp on pc.CID = pp.CID \
                        left join photo as p on pp.PhotoID = p.PhotoID \
                        left join userprofile as up on pc.UserID = up.UserID \
                        left join userprofile as up2 on share.UserID = up2.UserID \
                     where " \
                     "share.Share_status='Active' and " \
                     "share.UserID !='" + userid + "' and " \
                     "pc.Post_type ='Photo'"
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


def fetchvideo_others(userid):
    sql = "Select share.ShareID, pc.Post_type, v.Video_url, pc.Description, " \
                     "up.Name, pc.UserID, share.Share_describe, share.Share_dateTime, up2.Name, " \
                     "up.Profile_pic, pc.Post_status \
                     from share \
                        left join post_content as pc on share.CID = pc.CID \
                        left join post_video as pv on pc.CID = pv.CID \
                        left join video as v on pv.VideoID = v.VideoID \
                        left join userprofile as up on pc.UserID = up.UserID \
                        left join userprofile as up2 on share.UserID = up2.UserID \
                     where " \
                     "share.Share_status='Active' and " \
                     "share.UserID !='" + userid + "' and " \
                     "pc.Post_type ='Video'"
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


def fetchall(userid):
    share = []
    for x in fetchphoto_others(userid):
        a = list(x)
        a.append(post_content.Post_content.post_num(a[0], userid))
        a[7] = date_cal(a[7])
        b = tuple(a)
        share += [b]
    for y in fetchvideo_others(userid):
        a = list(y)
        a.append(post_content.Post_content.post_num(a[0], userid))
        a[7] = date_cal(a[7])
        b = tuple(a)
        share += [b]
    return share


def fetchphoto_user(userid):
    sql = "Select share.ShareID, pc.Post_type, p.Photo_url, pc.Post_status, share.Share_status \
                     from share \
                        left join post_content as pc on share.CID = pc.CID \
                        left join post_photo as pp on pc.CID = pp.CID \
                        left join photo as p on pp.PhotoID = p.PhotoID \
                     where " \
                     "share.UserID ='" + userid + "' and " \
                     "pc.Post_type ='Photo'"
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

def fetchvideo_user(userid):
    sql = "Select share.ShareID, pc.Post_type, v.Video_url, pc.Post_status, share.Share_status  \
                     from share \
                        left join post_content as pc on share.CID = pc.CID \
                        left join post_video as pv on pc.CID = pv.CID \
                        left join video as v on pv.VideoID = v.VideoID \
                     where " \
                     "share.UserID ='" + userid + "' and " \
                     "pc.Post_type ='Video'"
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



def fetchall_user(userid):
    share = []
    share += fetchphoto_user(userid)
    share += fetchvideo_user(userid)
    return share


def fetchone(sid, userid):
    types = request.args.get("type")
    cursor = conn.mydb.cursor(buffered=True)
    sql = "Select share.ShareID, pc.Post_type, {}.{}_url, pc.Description, up.Name, \
           pc.UserID, share.Share_describe, share.Share_dateTime, up2.Name, up2.Profile_pic, up2.UserID, pc.Post_status \
            from share \
                left join post_content as pc on share.CID = pc.CID \
                left join post_{} as p on pc.CID = p.CID \
                left join {} on p.{}ID = {}.{}ID \
                left join userprofile as up on pc.UserID = up.UserID \
                left join userprofile as up2 on share.UserID = up2.UserID \
            where \
                share.ShareID='{}'".format(types, types, types, types, types, types, types, sid)
    try:
        cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        a = list(cursor.fetchone())
        a.append(post_content.Post_content.post_num(a[0], userid))
        a[7] = date_cal(a[7])
        myresult = tuple(a)
    except:
        conn.mydb.ping(True)
        cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        a = list(cursor.fetchone())
        a.append(post_content.Post_content.post_num(a[0], userid))
        a[7] = date_cal(a[7])
        myresult = tuple(a)
    return myresult


def delete(sid):
    sql = "DELETE FROM `share` WHERE ShareID='{}'".format(sid)
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()
    pass


def update(sid, description):
    sql = "Update share set Share_describe='{}' where ShareID='{}'".format(description, sid)
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()
    pass

def update_status(sid, status):
    sql = "Update share set Share_status='{}' where ShareID='{}'".format(status, sid)
    try:
        mycursor.execute(sql)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
        conn.mydb.commit()
    pass


def fetchall_share():
    sql = "Select * from share " \
          "left join post_content as pc on share.CID = pc.CID"
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        shares = mycursor.fetchall()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        shares = mycursor.fetchall()
    return shares