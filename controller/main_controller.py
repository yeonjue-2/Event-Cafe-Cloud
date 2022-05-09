import jwt
from flask import request, render_template, Blueprint, jsonify, url_for, redirect

from database import DB
from ectoekn import ECTOKEN

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    user = ECTOKEN.get_token(object)
    if user is not None:
        cafes = DB.list('cafes', {}, {'_id': False})
        for cafe in cafes:
            cafe_idx = str(cafe['idx'])
            cafe["count_heart"] = DB.count_documents('hearts', {"cafe_idx": cafe_idx, "type": "heart"})
            cafe["heart_by_me"] = bool(
                DB.find_one('hearts', {"cafe_idx": cafe_idx, "type": "heart", "user_id": user["user_id"]},
                            {"_id": False}))
            cafe["count_bookmark"] = DB.count_documents('hearts', {"cafe_idx": cafe_idx, "type": "bookmark"})
            cafe["bookmark_by_me"] = bool(
                DB.find_one('hearts', {"cafe_idx": cafe_idx, "type": "bookmark", "user_id": user["user_id"]},
                            {"_id": False}))
        return render_template('index.html', user=user)
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
    # 포스팅 목록 받아오기
    for cafe in cafes:
        cafe_idx = str(cafe['idx'])
        cafe["count_heart"] = DB.count_documents('hearts', {"cafe_idx": cafe_idx, "type": "heart"})
        cafe["heart_by_me"] = bool(
            DB.find_one('hearts', {"cafe_idx": cafe_idx, "type": "heart", "user_id": user_id}, {"_id": False}))
        cafe["count_bookmark"] = DB.count_documents('hearts', {"cafe_idx": cafe_idx, "type": "bookmark"})
        cafe["bookmark_by_me"] = bool(
            DB.find_one('hearts', {"cafe_idx": cafe_idx, "type": "bookmark", "user_id": user_id}, {"_id": False}))
    return jsonify({"result": "success", "cafes": cafes, "user_id": user_id})


@bp.route('/update_like', methods=['POST'])
def update_heart():
    user_id = ECTOKEN.get_user_id(object)
    cafe_idx_receive = request.form["cafe_idx_give"]
    type_receive = request.form["type_give"]
    action_receive = request.form["action_give"]

    doc = {
        "cafe_idx": cafe_idx_receive,
        "user_id": user_id,
        "type": type_receive
    }

    if action_receive == "heart":
        DB.insert('hearts', doc)
    else:
        DB.delete('hearts', doc)

    count = DB.count_documents("hearts", {"cafe_idx": cafe_idx_receive, "type": type_receive})
    return jsonify({"result": "success", "count": count})
