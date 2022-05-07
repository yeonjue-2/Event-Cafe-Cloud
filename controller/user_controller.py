import jwt
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from controller.auth_controller import SECRET_KEY
from database import DB

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/profile')
def home():
    token = request.cookies.get("usertoken")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = DB.find_one("users", {"user_id": payload["user_id"]})
        print(user)
        return render_template('userProfile.html', user=user)
    except jwt.ExpiredSignatureError:
        return render_template('userProfile.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('userProfile.html', msg="로그인 정보가 없습니다!")


@bp.route('/api/update', methods=["POST"])
def update():
    token = request.cookies.get("usertoken")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload["user_id"]
        user_nickname = request.form['user_nickname_give']
        user_info = request.form['user_userinfo_give']
        user_profile = request.files['user_profile_give']

        extension = user_profile.filename.split('.')[-1]

        save_to = f'static/profile_pics/{user_id}.{extension}'
        user_profile.save(save_to)

        new_doc = {
            "user_nickname": user_nickname,
            "user_profile": f"{user_id}.{extension}",
            "user_info": user_info,
        }

        DB.update_one("users", {'user_id': user_id}, {'$set': new_doc})
        return jsonify({'result': 'success'})

    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
