import random, string
import conn
import datetime
from flask import request

id_generator = string.ascii_letters + string.digits
mycursor = conn.mydb.cursor()


class Report:
    def __init__(self, ReportID, AdminID):
        self.ReportID = ReportID
        self.AdminID = AdminID

    def create(self):
        sql = "Insert into report (ReportID, Report_status) values (%s, %s)"
        val = (self.ReportID, "InProgress")
        try:
            mycursor.execute(sql, val)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql, val)
            conn.mydb.commit()
        return 'Create Report Success'

    def update(self):
        sql = "Update report set AdminID='{}', Report_status='{}' where RID='{}'".format(self.AdminID, self, self)
        try:
            mycursor.execute(sql)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
            conn.mydb.commit()
        return 'Update Report Success'

    def remove(self):
        sql = "Update report set AdminID=Null, Report_status='InProgress', " \
              "Progress_start=Null, Progress_end=Null where RID='{}'".format(self)
        try:
            mycursor.execute(sql)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
            conn.mydb.commit()
        return 'Remove Report Success'

    def completed(self):
        sql = "Update report set Report_status='Completed', Progress_end='{}' where RID='{}'".format(datetime.datetime.now(), self)
        try:
            mycursor.execute(sql)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
            conn.mydb.commit()
        return 'Complete Report Success'

    def handle(self):
        sql = "Update report set AdminID='{}', Report_status='{}', Progress_start='{}' where ReportID='{}' "\
            .format(self.AdminID, "InProgress", datetime.datetime.now(), self.ReportID)
        try:
            mycursor.execute(sql)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql)
            conn.mydb.commit()
        return 'Handle Report Success'

    def fetchone(self):
        sql = "Select Distinct * from report where RID='{}'".format(self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            report = cursor.fetchone()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            report = cursor.fetchone()
        return report

    def fetchall(self):
        sql = "Select * from report where AdminID='{}' order by Report_Status DESC".format(self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            report = cursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            report = cursor.fetchall()
        return report

    def method_request(self):
        if request.method == "POST":
            report = Report.create(self)
            return report


class Report_info:
    def __init__(self, cid, Report_Detail, UserID):
        self.reportID = 'R_' + ''.join(random.choice(id_generator) for i in range(5))
        self.cid = cid
        self.detail = Report_Detail
        self.dateTime = datetime.datetime.now()
        self.uid = UserID

    def create(self):
        sql = "Insert into report_info (ReportID, CID, ReportDetail, Report_datetime, UserID) values " \
              "(%s, %s, %s, %s, %s)"
        val = (self.reportID, self.cid, self.detail, self.dateTime, self.uid)
        try:
            mycursor.execute(sql, val)
            conn.mydb.commit()
        except:
            conn.mydb.ping(True)
            mycursor.execute(sql, val)
            conn.mydb.commit()
        return self.reportID

    def fetchone(self):
        sql = "Select * from report_info where ReportID='{}'".format(self)
        cursor = conn.mydb.cursor(buffered=True)
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            info = cursor.fetchone()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            cursor.execute(sql)
            info = cursor.fetchone()
        return info

    def fetchall(self):
        sql = "Select report_info.ReportID, report_info.CID, report_info.ReportDetail, " \
              "report_info.Report_datetime, report_info.UserID, pc.Post_type " \
              "from report_info " \
              "left join report on report.ReportID = report_info.ReportID " \
              "left join post_content as pc on pc.CID = report_info.CID " \
              "where report.AdminID is Null"
        try:
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            info = mycursor.fetchall()
        except:
            conn.mydb.ping(True)
            mycursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ")
            mycursor.execute(sql)
            info = mycursor.fetchall()
        return info

    def method_request(self):
        if request.method == "POST":
            reportID = Report_info.create(self)
            return reportID
        elif request.method == "GET":
            info = Report_info.fetchone(self)
            return info
