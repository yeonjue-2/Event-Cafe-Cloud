from datetime import datetime

from flask import Blueprint, jsonify, render_template, request
from database import DB
from ectoken import ECTOKEN

bp = Blueprint('cafe', __name__)


@bp.route('/cafe/detail')
def routeCafeDetail():
    return render_template('cafeDetail.html')


@bp.route('/api/cafe/detail/<cafeId>')
def getCafeDetail(cafeId):
    cafes = DB.find_one('cafes', {'idx': int(cafeId)}, {'_id': False})
    events = DB.list('event', {'cafe_id': cafeId}, {'_id': False})
    reviews = []
    for event in events:
        review = DB.list('reviews', {'event_id': event['event_id']}, {'_id': False})
        reviews.append(review)
    response = {
        'cafes': cafes,
        'reviews': reviews
    }
    return jsonify(response)


@bp.route('/api/cafe/review', methods=["POST"])
def regCafeReview():
    user_id = ECTOKEN.get_user_id(object)
    cafe_idx = request.form['cafe_idx_give']
    cafe_rating = request.form['cafe_rating_give']
    cafe_review = request.form['cafe_review_give']

    today = datetime.now()
    create_date = today.strftime('%Y-%m-%d-%H-%M-%S')

    reviews_count = DB.count_collection("reviews")
    if reviews_count == 0:
        max_value = 1
    else:
        max_value = DB.idx_plus("reviews")

    doc = {
        "review_id": max_value,
        "user_id": user_id,
        "cafe_id": cafe_idx,
        "cafe_review": cafe_review,
        "cafe_rating": cafe_rating,
        "create_date": create_date
    }

    DB.insert(collection="reviews", data=doc)
    return jsonify({'result': 'success'})
