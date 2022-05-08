import jwt
from flask import request, render_template, Blueprint, jsonify, url_for, redirect

from database import DB
from controller.auth_controller import SECRET_KEY

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    token = request.cookies.get("usertoken")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = DB.find_one("users", {"user_id": payload["user_id"]})
        return render_template('index.html', user=user)
    except jwt.ExpiredSignatureError:
        return render_template('index.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('index.html', msg="로그인 정보가 없습니다!")


@bp.route('/main', methods=['GET'])
def show_cafes():
    msg = request.args.get('msg')
    cafes = DB.list('cafes', {}, {'_id': False})
    return jsonify({'result': 'success', 'cafes': cafes})


@bp.route("/listing", methods=['GET'])
def listing():
    token = request.cookies.get("usertoken")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        # user = DB.find_one("users", {"user_id": payload["user_id"]})
        cafes = DB.list('cafes', {}, {'_id': False})
        print(cafes)

        # 포스팅 목록 받아오기
        for cafe in cafes:
            cafe["_id"] = str(cafe["_id"])
            cafe["count_heart"] = DB.count_documents('users', {"cafe_id": cafe["_id"]}, {"type": "heart"})
            cafe["heart_by_me"] = bool(DB.find_one('hearts', {"cafe_id": cafe["_id"]}, {"type": "heart"}, {"user_id": payload["user_id"]}))
            cafe["bookmark_by_me"] = bool(DB.find_one('hearts', {"cafe_id": cafe["_id"]}, {"type": "bookmark"}, {"user_id": payload["user_id"]}))
        return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", 'cafes': cafes})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))


@bp.route('/update_like', methods=['POST'])
def update_heart():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = DB.find_one("users", {"user_id": payload["user_id"]})
        cafe_id_receive = request.form["cafe_id_give"]
        type_receive = request.form["type_give"]
        action_receive = request.form["action_give"]
        print(cafe_id_receive, type_receive, action_receive)

        doc = {
            "cafe_id": cafe_id_receive,
            "user_id": user["user_id"],
            "type": type_receive
        }

        if action_receive == "heart":
            DB.insert_one('hearts', doc)
        else:
            DB.delete_one('hearts', doc)
        count = DB.count_documents({"cafe_id": cafe_id_receive}, {"type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})
    except (jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))
