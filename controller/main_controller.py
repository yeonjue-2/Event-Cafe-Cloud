import jwt
from flask import request, render_template, Blueprint, jsonify, url_for, redirect

from database import DB
from controller.auth_controller import SECRET_KEY
from ectoekn import ECTOKEN

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    user = ECTOKEN.get_token(object)
    if user is not None:
        cafes = DB.list('cafes', {}, {'_id': False})
        return render_template('index.html', user=user, cafes=cafes)
    else:
        return render_template('index.html', msg="로그인 정보가 없습니다")



@bp.route('/api/main', methods=['GET'])
def show_cafes():
    msg = request.args.get('msg')
    cafes = DB.list('cafes', {}, {'_id': False})
    return jsonify({'result': 'success', 'cafes': cafes})


@bp.route("/listing", methods=['GET'])
def listing():
    user_id = ECTOKEN.get_user_id(object)
    cafes = DB.list('cafes', {}, {'_id': False})
    print(cafes)

    # 포스팅 목록 받아오기
    for cafe in cafes:
        cafe_idx = cafes["idx"]
        cafe["count_heart"] = DB.count_documents('users', {"cafe_idx": cafe_idx}, {"type": "heart"})
        cafe["heart_by_me"] = bool(DB.find_one('hearts', {"cafe_idx": cafe_idx}, {"type": "heart"}, {"user_id": user_id}))
        cafe["bookmark_by_me"] = bool(DB.find_one('hearts', {"cafe_idx": cafe_idx}, {"type": "bookmark"}, {"user_id": user_id}))
    return jsonify({"result": "success", "msg": "포스팅을 가져왔습니다.", 'cafes': cafes})



@bp.route('/update_like', methods=['POST'])
def update_heart():
    user_id = ECTOKEN.get_user_id(object)
    cafe_id_receive = request.form["cafe_id_give"]
    type_receive = request.form["type_give"]
    action_receive = request.form["action_give"]
    print(cafe_id_receive, type_receive, action_receive)

    doc = {
        "cafe_id": cafe_id_receive,
        "user_id": user_id,
        "type": type_receive
    }

    if action_receive == "heart":
        DB.insert_one('hearts', doc)
    else:
        DB.delete_one('hearts', doc)
        count = DB.count_documents({"cafe_id": cafe_id_receive}, {"type": type_receive})
        return jsonify({"result": "success", 'msg': 'updated', "count": count})




