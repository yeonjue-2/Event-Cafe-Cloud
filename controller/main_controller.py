import jwt
from flask import request, render_template, Blueprint, jsonify, url_for, redirect

from database import DB
from ectoken import ECTOKEN
from type.collection import Collection

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    user = ECTOKEN.get_token()
    if user is not None:
        cafes = DB.list(Collection.CAFES, {}, {'_id': False})
        for cafe in cafes:

            cafe_idx = str(cafe['idx'])
            cafe["count_heart"] = DB.count_documents(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "heart"})
            cafe["heart_by_me"] = bool(DB.find_one(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "heart", "user_id": user["user_id"]},{'_id': False}))
            cafe["bookmark_by_me"] = bool(DB.find_one(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "bookmark", "user_id": user["user_id"]},{'_id': False}))

        return render_template('index.html', user=user)
    else:
        return render_template('index.html', msg="로그인 정보가 없습니다")


@bp.route('/event_cafe/<event_category>')
def event_cafe(event_category):
    user = ECTOKEN.get_token()

    if user is not None:
        return render_template('eventCafe.html', user=user, event_category=event_category)
    else:
        return render_template('eventCafe.html', msg="로그인 정보가 없습니다")

@bp.route('/listing', methods=['GET'])
def listing():
    user_id = ECTOKEN.get_user_id()
    cafes = DB.list(Collection.CAFES, {}, {'_id': False})

    for cafe in cafes:
        cafe_idx = str(cafe['idx'])
        cafe["count_heart"] = DB.count_documents(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "heart"})
        cafe["heart_by_me"] = bool(DB.find_one(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "heart", "user_id": user_id}, {'_id': False}))
        cafe["bookmark_by_me"] = bool(DB.find_one(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "bookmark", "user_id": user_id}, {'_id': False}))

    return jsonify({"result": "success", "cafes": cafes})

@bp.route('/event_cafe/listing_event', methods=['GET'])
def listing_event():
    user_id = ECTOKEN.get_user_id()

    event_category_receive = request.args.get("event_category_give")
    events = DB.list(Collection.EVENTS, {"event_category": event_category_receive}, {'_id': False})
    cafes = []

    for event in events:
        cafe_id = int(event['cafe_id'])
        cafe = DB.find_one(Collection.CAFES, {"idx": cafe_id}, {'_id': False})
        cafe_name = cafe['cafe_name']
        event['cafe_name'] = cafe_name
        cafes.append(cafe)

    for cafe in cafes:
        cafe_idx = str(cafe['idx'])
        cafe["count_heart"] = DB.count_documents(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "heart"})
        cafe["heart_by_me"] = bool(DB.find_one(Collection.HEARTS, {"cafe_idx": cafe_idx, "type": "heart", "user_id": user_id}, {'_id': False}))

    return jsonify({"result": "success", "cafes": cafes, "events": events})

@bp.route('/update_heart', methods=['POST'])
def update_heart():
    user_id = ECTOKEN.get_user_id()
    cafe_idx_receive = request.form["cafe_idx_give"]
    type_receive = request.form["type_give"]
    action_receive = request.form["action_give"]

    doc = {
        "user_id": user_id,
        "cafe_idx": cafe_idx_receive,
        "type": type_receive
    }

    if action_receive == "heart":
        DB.insert(Collection.HEARTS, doc)
    else:
        DB.delete(Collection.HEARTS, doc)

    count = DB.count_documents(Collection.HEARTS, {"cafe_idx": cafe_idx_receive, "type": type_receive})
    return jsonify({"result": "success", "count": count})
