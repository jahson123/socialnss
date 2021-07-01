import mysql.connector
from flask import request

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="snss")
mycursor = mydb.cursor(buffered=True)


def check_like(cid):
    sql = "SELECT count(CID) as NumPostLike from `like` WHERE CID='" + cid + "' "
    cursor = mydb.cursor(buffered=True)
    cursor.execute(sql)
    like = cursor.fetchone()
    return like[0]


def check_user_like(userid, cid):
    sql = "Select UserID from `like` WHERE UserID ='{}' and CID='{}'".format(userid, cid)
    mycursor.execute(sql)
    result = mycursor.fetchone()
    mydb.commit()
    if result == None:
        return None
    elif result[0] == userid:
        return result[0]


def like(user_id, cid):
    sql = "INSERT INTO `like` (`UserID`, `CID`) VALUES (%s, %s)"
    val = (user_id, cid)
    mycursor.execute(sql, val)
    mydb.commit()
    return 'Like'


def unlike(user_id, cid):
    sql = "DELETE FROM `like` WHERE CID='" + cid + "' and UserID='" + user_id + "'"
    mycursor.execute(sql)
    mydb.commit()
    return "Dislike"

def delete(cid):
    sql = "DELETE FROM `like` WHERE CID='{}'".format(cid)
    mycursor.execute(sql)
    mydb.commit()


def fetchall():
    sql = "Select like.LikeID, like.UserID, like.CID, pc.Post_type from `like` " \
          "left join post_content as pc on like.CID = pc.CID"
    mycursor.execute(sql)
    likes = mycursor.fetchall()
    return likes

def request_like(user_id, cid):
    if request.method == "POST":
        like(user_id, cid)
    elif request.method == "DELETE":
        unlike(user_id, cid)
