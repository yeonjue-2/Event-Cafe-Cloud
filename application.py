from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager

client = MongoClient('localhost', 27017)
db = client.event_cafe_cloud

SECRET_KEY = 'MYCC'

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/join')
def join_form():
    return render_template("join.html")

@app.route('/login')
def login_form():
    return render_template("login.html")

@app.route("/api/join", methods=["POST"])
def join():
    user_id = request.form['user_id_give']
    password = request.form['user_pw_give']
    user_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user_email = request.form['user_email_give']
    user_nickname = request.form['user_nickname_give']
    user_profile = request.files['user_profile_give']

    extension = user_profile.filename.split('.')[-1]

    today = datetime.now()
    ptime = today.strftime('%Y-%m-%d-%H-%M-$S')

    profile_img = f'user_profile-{ptime}'

    save_to = f'static/profile_pics/{profile_img}.{extension}'
    user_profile.save(save_to)

    doc = {
        "user_id": user_id,
        "user_pw": user_pw,
        "user_email": user_email,
        "user_nickname": user_nickname,
        "user_profile": f"{profile_img}/{extension}",
    }
    db.users.insert_one(doc)
    return jsonify({'result':'success'})

@app.route("/api/join/double_check", methods=["POST"])
def double_check():
    user_id = request.form['user_id_give']
    checkResult = bool(db.users.find_one({"user_id":user_id}))
    return jsonify({'result': 'success', 'checkResult': checkResult})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5002, debug=True)