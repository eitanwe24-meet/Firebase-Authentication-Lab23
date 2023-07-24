from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
import datetime

config = {
  "apiKey": "AIzaSyDG2Wte4WO76rYkOSgJTxWpQZVLBEwBscE",
  "authDomain": "eitanw12345.firebaseapp.com",
  "projectId": "eitanw12345",
  "storageBucket": "eitanw12345.appspot.com",
  "messagingSenderId": "85868299687",
  "appId": "1:85868299687:web:566d3582ac4623b920a282",
  "measurementId": "G-T3SXKGG9PN",
  "databaseURL": "https://eitanw12345-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['nameStr']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'name':name, 'username': username, 'bio':bio, 'email':email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"

    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    erorr = ""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        name = request.form['nameStr']
        username = request.form['username']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {'name':name, 'username': username, 'bio':bio, 'email':email}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed  "
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        text = request.form['text']
        title = request.form['title']
        try:
            ct = str(datetime.datetime.now())
            UID = login_session['user']['localId']
            tweet = {'text':text , 'uid' : UID, 'title':title,'time':ct}
            db.child("Tweets").push(tweet)

        except Exception as e:
            print(e)
            erorr = "fwenovww"
    return render_template("add_tweet.html")

@app.route('/sign_out')
def signout():
    
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/all_tweets')
def alltweets():
    tweets = db.child("Tweets").get().val()
    return render_template("tweets.html", tweets = tweets)

if __name__ == '__main__':
    app.run(debug=True)