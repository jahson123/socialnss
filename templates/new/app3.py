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

@app.route('/', methods=['GET', 'POST'])
def mainpage():
    if request.method == "POST":
        docs = db.collection('Users').stream()
        username = request.form.get('uname')
        pwd = request.form.get('pwd')
        for doc in docs:
            user = doc.to_dict()
            if user['username'] == username and user['password'] == pwd:
                return redirect('/homepage')
        else:
            return 'Fail'

    return render_template("loginpage.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup_request():
    if request.method == "POST":
        username = request.form.get('uname')
        pwd = request.form.get('pwd')
        email = request.form.get('email')
        uid_generator = string.ascii_letters + string.digits
        user_id = ''.join(random.choice(uid_generator) for i in range(6))
        user_doc = db.collection('Users').document(user_id)
        user_doc.set({
            'username': username,
            'password': pwd,
            'email': { 'email': email, 'email_verified': False }
        })
        send_email.email(email, user_id)
    return render_template('signup.html')

@app.route('/emailverified/<uid>')
def email_verified(uid):
    user_doc = db.collection('Users').document(uid)
    user_doc.update({'email.email_verified': True})
    return redirect('/')

@app.route('/homepage')
def homepage():
    storage = pb.storage()
    image_docs = db.collection('Image').stream()
    for doc in image_docs:
        image_id = doc.to_dict()
        image_url = image_id['Image_url']
    return render_template('/homepage.html')

@app.route('/image', methods=['POST', 'GET'])
def image():
    if request.method == "POST":
        file = request.files.get('img')
        img_name = file.filename
        storage = pb.storage()
        path_on_cloud = "images/" + img_name
        storage.child(path_on_cloud).put(file)
        image_id_generator = string.ascii_letters + string.digits
        img_id = ''.join(random.choice(image_id_generator) for i in range(6))
        user_doc = db.collection('Images').document('Small_image')
        user_doc.set({
            'Image_id': "S_img_"+img_id,
            'Image_url': storage.child("images/"+img_name).get_url(None),
        })
        return 'Success'
    return render_template("image.html")

@app.route('/images')
def get_image():
    docs = db.collection('Images').stream()
    image_doc = {}
    for doc in docs:
        image = doc.to_dict()
        image_doc.update( {doc.id:{
            'image_id': image['Image_id'],
            'image_url': image['Image_url'],
        }})
    return render_template("image.html", image_docs=image_doc.values())


@app.route('/test')
def test():
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
    return render_template('test.html', doc_test=doc_dict.values())

if __name__ == "__main__":
    app.run(debug=True)
