from flask import *
import random,string
import pyrebase
import firebase_admin
from firebase_admin import credentials, db, auth, firestore, storage
import send_email


cred = credentials.Certificate("firebase-sdk.json")
firebase = firebase_admin.initialize_app(cred,
{
    "databaseURL": "https://unique-perigee-299514-default-rtdb.firebaseio.com/",
    "storageBucket": "unique-perigee-299514.appspot.com",
})

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

db = firestore.client()
app = Flask(__name__)

""""


# get_image_url
storage = pb.storage()
a= storage.child("images/dsad.png").get_url(None)
print(a)
"""
"""
file = "connect.png"
bucket = storage.bucket()
blob = bucket.blob(file)
blob.upload_from_file(file)
print(blob)
"""
""""
docs = db.collection('Users').stream()
doc_dict = {}
for doc in docs:
    user = doc.to_dict()
    id = doc.id
    doc_dict.update({id:
        {
            'username': user['username'],
            'email': user['email'],
            'password': user['password']
        }})
"""
""""
image_docs = db.collection('Images').document('Small_image').get()
doc = image_docs.to_dict()
print(doc)
url = doc['Image_url']
print(url)
"""

"""
docs = db.collection('Images').stream()
image_doc = {}
for doc in docs:
    image = doc.to_dict()
    image_doc.update({
            'image_id': image['Image_id'],
            'mage_url': image['Image_url'],
    })
print(image_doc)
for a in image_doc.values():
    print(a.Image_id)
"""
