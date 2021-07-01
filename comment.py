import mysql.connector
from flask import request

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="snss")
mycursor = mydb.cursor(buffered=True)


def comment(comment, user_id, cid):
    if request.method == "POST":
        sql = "INSERT INTO `comment` (Comment, CID, UserID) VALUES (%s, %s, %s)"
        val = (comment, cid, user_id)
        mycursor.execute(sql, val)
        mydb.commit()
        return 'Comment'

def delete_comment(comment_id, user_id):
    if request.method == "DELETE":
        sql = "DELETE FROM `comment` WHERE CommentID='{}' and UserID='{}'".format(comment_id, user_id)
        mycursor.execute(sql)
        mydb.commit()
        return 'Comment Deleted'


def delete(cid):
    sql = "DELETE FROM `comment` WHERE CID='{}'".format(cid)
    mycursor.execute(sql)
    mydb.commit()
    pass

def comment_edit(comment_id, comment):
    if request.method == "PATCH":
        sql = "Update `comment` set Comment='" + comment + "' where CommentID='" + str(comment_id) + "'"
        mycursor.execute(sql)
        mydb.commit()
        return 'Comment Updated'

def comment_list(cid):
    if request.method == "GET":
        sql = "SELECT c.CommentID, c.Comment, c.CID, c.UserID , up.Name, up.Profile_pic " \
              "from `comment` as c " \
              "left join userprofile as up on c.UserID = up.UserID " \
              "WHERE c.CID='{}'".format(cid)
        mycursor.execute(sql)
        comment = mycursor.fetchall()
        return comment

def check_comment(cid):
    sql = "SELECT count(CID) as NumPostComment from `comment` WHERE CID='" + cid + "' "
    cursor = mydb.cursor(buffered=True)
    cursor.execute(sql)
    num = cursor.fetchone()
    return num[0]

def fetchall():
    sql = "Select * from `comment`"
    mycursor.execute(sql)
    comments = mycursor.fetchall()
    return comments

def fetchone(id):
    sql = "SELECT * from comment where CommentID='{}'".format(id)
    cursor = mydb.cursor(buffered=True)
    cursor.execute(sql)
    comment = cursor.fetchone()
    return comment