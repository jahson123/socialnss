import mysql.connector
import pyrebase
from flask import *
from like import check_like
from share import check_share
import post_content
import random
import video, share, photo, like, comment
from date_calc import date_cal

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="snss"
)

mycursor = mydb.cursor(buffered=True)

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

import follow

def test(self1 ,self2):
    relate = follow.check_relation(self1, self2)
    return relate

print(test("UNDQ24", "FWIlBX"))