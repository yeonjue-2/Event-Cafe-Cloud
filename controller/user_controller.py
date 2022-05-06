import jwt
from flask import Blueprint, request, render_template

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


@bp.route('/api/update', methods=["PUT"])
def update():
    user_nickname = request.form['user_nickname_give']
    user_info = request.form['user_userinfo_give']
    user_profile = request.form['user_profile_give']

    token = request.get.cookies.get("usertoken")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = payload["user_id"]
        return user_id
    except jwt.ExpiredSignatureError:
        return "로그인 시간 만료"
    except jwt.exceptions.DecodeError:
        return "로그인 정보 없음"

    extension = user_profile.filename.split('.')[-1]

    save_to = f'static/profile_pics/{user_id}.{extension}'
    user_profile.save(save_to)

    DB.update_one("users", {'user_id': user_id}, {'$set': {'user_profile': user_profile}})
    DB.update_one("users", {'user_id': user_id}, {'$set': {'user_info': user_info}})

    return jsonify({'result': 'success'})