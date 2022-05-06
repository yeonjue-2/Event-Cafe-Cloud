from pymongo import MongoClient
import jwt
import datetime
import hashlib
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from database import DB

SECRET_KEY = 'MYCC'

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/')
def home():
    token = request.cookies.get("usertoken")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = DB.find_one("users", {"user_id": payload["user_id"]})
        print(user)
        return render_template('index.html', user=user)
    except jwt.ExpiredSignatureError:
        return render_template('index.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('index.html', msg="로그인 정보가 없습니다!")

@bp.route('/join')
def join_form():
    return render_template("join.html")


@bp.route('/login')
def login_form():
    msg = request.args.get('msg')
    return render_template("login.html", msg=msg)


@bp.route("/api/join", methods=["POST"])
def join():
    user_id = request.form['user_id_give']
    password = request.form['user_pw_give']
    user_pw = hashlib.sha256(password.encode('utf-8')).hexdigest()
    user_email = request.form['user_email_give']
    user_nickname = request.form['user_nickname_give']
    user_profile = request.files['user_profile_give']

    extension = user_profile.filename.split('.')[-1]

    save_to = f'static/profile_pics/{user_id}.{extension}'
    user_profile.save(save_to)

    doc = {
        "user_id": user_id,
        "user_pw": user_pw,
        "user_email": user_email,
        "user_nickname": user_nickname,
        "user_profile": f"{user_id}/{extension}",
    }
    DB.insert(collection="users", data=doc)
    return jsonify({'result': 'success'})


@bp.route("/api/join/double_check", methods=["POST"])
def double_check():
    user_id = request.form['user_id_give']
    checkResult = bool(DB.find_one("users", {"user_id": user_id}))
    return jsonify({'result': 'success', 'checkResult': checkResult})


@bp.route("/token_login", methods=["POST"])
def login():
    user_id = request.form["user_id_give"]
    pw = request.form["user_pw_give"]
    user_pw = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    result = DB.find_one("users", {'user_id': user_id, 'user_pw': user_pw})
    user_nickname = result['user_nickname']

    if result is not None:
        payload = {
            'user_id': user_id,
            'user_nickname': user_nickname,
            'exp': datetime.utcnow() + timedelta(seconds=60*60*24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '로그인 정보를 다시 확인해주세요'})

