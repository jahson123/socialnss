import conn
from flask import request

mycursor = conn.mydb.cursor()


class Follow:
    def __init__(self, user_1, user_2):
        self.u1 = user_1
        self.u2 = user_2

    def create(self):
        sql = "Insert into relationship (UserID_1, UserID_2, Relationship) values (%s, %s, %s)"
        val = (self.u1, self.u2, "Following")
        mycursor.execute(sql, val)
        conn.mydb.commit()

    def block(self):
        sql = "INSERT INTO relationship (UserID_1, UserID_2) \
               SELECT DISTINCT '{}', '{}' FROM relationship \
               WHERE NOT EXISTS ( SELECT * FROM relationship where UserID_1='{}' and UserID_2 ='{}' LIMIT 1); \
               UPDATE relationship set Relationship='Blocked' where UserID_1='{}' and UserID_2 ='{}'".format(self.u1, self.u2, self.u1, self.u2, self.u1, self.u2)
        try:
            for _ in mycursor.execute(sql, multi=True):
                pass
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            for _ in mycursor.execute(sql, multi=True):
                pass
            conn.mydb.commit()

    def unblock(self):
        sql = "UPDATE relationship set Relationship='Following' where RelateID='{}'".format(self)
        try:
            mycursor.execute(sql)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
            conn.mydb.commit()

    def delete(self):
        sql = "Delete from relationship where RelateID='{}'".format(self)
        try:
            mycursor.execute(sql)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
            conn.mydb.commit()


    def fetchall(self):
        sql = "Select * from relationship"
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            relation = mycursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            relation = mycursor.fetchall()
        return relation

    def fetchall_user(self):
        sql = "Select Distinct * from relationship where UserID_1='{}' or UserID_2='{}'".format(self, self)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            relation = mycursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            relation = mycursor.fetchall()
        return relation

    def fetchall_following(self):
        sql = "Select Distinct r.RelateID, r.UserID_2, up.Name, up.Profile_pic " \
              "from relationship as r " \
              "left join userprofile as up on up.UserID = r.UserID_2 " \
              "where r.UserID_1='{}' and r.Relationship='Following'".format(self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            follower = cursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            follower = cursor.fetchall()
        return follower

    def fetchall_follower(self):
        sql = "Select Distinct r.RelateID, r.UserID_1, up.Name, up.Profile_pic " \
              "from relationship as r " \
              "left join userprofile as up on up.UserID = r.UserID_1 " \
              "where r.UserID_2='{}' and r.Relationship='Following'".format(self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            follower = cursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            follower = cursor.fetchall()
        return follower

    def suggestion(self):
        sql = "Select Distinct user.UserID, up.Name, up.Profile_pic from user " \
              "left join relationship as r on r.UserID_1 = user.UserID " \
              "left join userprofile as up on up.UserID = user.UserID " \
              "where " \
              "user.UserID not in (Select UserID_2 from relationship where UserID_1='{}') and " \
              "user.UserID not in (Select UserID_1 from relationship where UserID_1='{}') and " \
              "user.UserID !='{}'".format(self, self, self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            suggest = cursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            suggest = cursor.fetchall()
        return suggest

    def count_following(self):
        sql = "Select Count(UserID_2) from relationship where UserID_1='{}' and Relationship='Following'".format(self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            following_num = cursor.fetchone()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            following_num = cursor.fetchone()
        return following_num[0]

    def count_followers(self):
        sql = "Select Count(UserID_1) from relationship where UserID_2='{}' and Relationship='Following'".format(self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            followers_num = cursor.fetchone()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            followers_num = cursor.fetchone()
        return followers_num[0]

    def relationship_num(self):
        num = [Follow.count_followers(self), Follow.count_following(self)]
        return num

    def method_request(self):
        if request.method == "POST":
            Follow.create(self)
            return 'POST Success'
        if request.method == "DELETE":
            Follow.delete(self)
            return 'DELETE Success'

def check_relation(uid1, uid2):
    sql = "Select Distinct RelateID, relationship from relationship " \
          "where UserID_1='{}' and UserID_2='{}'".format(uid1, uid2)
    cursor = conn.mydb.cursor(buffered=True)
    try:
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        relate = cursor.fetchone()
    except:
        conn.mydb.ping(True)
        mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
        cursor.execute(sql)
        relate = cursor.fetchone()
    return relate
