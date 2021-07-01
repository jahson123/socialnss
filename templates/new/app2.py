from flask import *
import pyrebase
import firebase_admin
from firebase_admin import credentials, db, auth
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

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("loginpage.html")


users = [{'uid': 1, 'name': 'Noah Schairer'}]


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        user = auth.create_user(email=email, password=pwd, email_verified=False)
        ref = firebase.reference("users")

        send_email.email(email, user.uid)
    return render_template('signup.html')


""""
def basic():
    if request.method == "POST":
        user = db.reference("user")
        num = user.order_by_key().get()
        id = len(num)
        user.child(str(id)).set(
            {
                "username": request.form['uname'],
                "password": request.form['pwd']
            }
        );
    return render_template("loginpage.html")

@app.route('/signin', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = db.reference("user")
        num = user.order_by_key().get()
        id = len(num)
        for nums in range(id):
            uname = user.child(str(nums)).child("username").get()
            pwd = user.child(str(nums)).child("password").get()
            if request.form['uname'] == uname and request.form['pwd'] == pwd:
                return redirect("/homepage")
    return redirect("/")

@app.route('/homepage')
def homepage():
    return render_template("homepage.html")
"""


@app.route('/token', methods=['GET', 'POST'])
def token():
    if request.method == "POST":
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        user = pb.auth().sign_in_with_email_and_password(email, pwd)
        a = pb.auth().get_account_info(user['idToken'])
        if a['users'][0]['emailVerified'] == True:
            return 'Success'
        """
        jwt = user['idToken']
        return {'token': jwt}, 200
        """
        return 'False'
    return redirect("/")


@app.route('/emailverified/<uid>')
def email_verified(uid):
    user = auth.update_user(uid, email_verified=True)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)

