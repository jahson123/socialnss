import random,string
import conn

mycursor = conn.mydb.cursor()

def content_photo(pid):
    cid_generator = string.ascii_letters + string.digits
    cid = 'P_' + ''.join(random.choice(cid_generator) for i in range(6))
    sql = "Insert into content_type (CID, PhotoID) values (%s, %s)"
    val = (cid, pid)
    try:
        mycursor.execute(sql, val)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql, val)
        conn.mydb.commit()
    return cid

def content_video(vid):
    cid_generator = string.ascii_letters + string.digits
    cid = 'P_' + ''.join(random.choice(cid_generator) for i in range(6))
    sql = "Insert into content_type (CID, VideoID) values (%s, %s)"
    val = (cid, vid)
    try:
        mycursor.execute(sql, val)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql, val)
        conn.mydb.commit()
    return cid











