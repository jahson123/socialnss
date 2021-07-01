import conn
from flask import request

mycursor = conn.mydb.cursor(buffered=True)


def check_like(cid):
    sql = "SELECT count(CID) as NumPostLike from `like` WHERE CID='" + cid + "' "
    cursor = conn.mydb.cursor(buffered=True)
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        like = cursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        like = cursor.fetchone()
    return like[0]


def check_user_like(userid, cid):
    sql = "Select UserID from `like` WHERE UserID ='{}' and CID='{}'".format(userid, cid)
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        result = mycursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        result = mycursor.fetchone()
    if result == None:
        return None
    elif result[0] == userid:
        return result[0]


def like(user_id, cid):
    sql = "INSERT INTO `like` (`UserID`, `CID`) VALUES (%s, %s)"
    val = (user_id, cid)
    try:
        mycursor.execute(sql, val)
        conn.mydb.commit()
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql, val)
        conn.mydb.commit()
    return 'Like'


def unlike(user_id, cid):
    sql = "DELETE FROM `like` WHERE CID='{}' and UserID='{}'".format(cid, user_id)
    try:
        mycursor.execute(sql)
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
    conn.mydb.commit()
    return "Dislike"


def delete(cid):
    sql = "DELETE FROM `like` WHERE CID='{}'".format(cid)
    try:
        mycursor.execute(sql)
    except:
        conn.mydb.ping(True)
        mycursor.execute(sql)
    conn.mydb.commit()


def fetchall():
    sql = "Select like.LikeID, like.UserID, like.CID, pc.Post_type from `like` " \
          "left join post_content as pc on like.CID = pc.CID"
    try:
        mycursor.execute(sql)
        likes = mycursor.fetchall()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        mycursor.execute(sql)
        likes = mycursor.fetchall()
    return likes


def request_like(user_id, cid):
    if request.method == "POST":
        like(user_id, cid)
    elif request.method == "DELETE":
        unlike(user_id, cid)
