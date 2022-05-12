from datetime import datetime

from flask import Blueprint, jsonify, render_template, request, Response
from database import DB
from ectoken import ECTOKEN
from type.collection import Collection


bp = Blueprint('cafe', __name__)


@bp.route('/cafe/detail')
def routeCafeDetail():
    cafe_id = int(request.args.get('id'));
    user = ECTOKEN.get_token();
    if DB.find_one(Collection.CAFES,{Collection.CAFES_PK:cafe_id},{'_id':False}) is None:
        return Response(status = 404)
    if user is None:
        return render_template('cafeDetail.html', msg="로그인 정보가 없습니다")
    return render_template('cafeDetail.html',user=user)

@bp.route('/cafe/reservation/<cafe_id>', methods=['get'])
def get_event_info(cafe_id):
    user = ECTOKEN.get_token();
    if user is None:
        return render_template('index.html', msg="로그인 정보가 없습니다")
    return render_template('cafeReservation.html')

@bp.route('/api/cafe/detail/<cafeId>')
def getCafeDetail(cafeId):

    cafes = DB.find_one(Collection.CAFES, {Collection.CAFES_PK: int(cafeId)}, {'_id': False})
    reviews = DB.list(Collection.REVIEWS, {Collection.CAFES_PK: cafeId}, {'_id': False})

    response = {
        'cafes': cafes,
        'reviews': reviews
    }
    return jsonify(response)


@bp.route('/api/cafe/regReview', methods=["POST"])
def regCafeReview():
    user_id = ECTOKEN.get_user_id()
    cafe_idx = request.form['cafe_idx_give']
    cafe_rating = request.form['cafe_rating_give']
    cafe_review = request.form['cafe_review_give']

    reviewFlag = DB.find_one(Collection.REVIEWS,{Collection.USERS_PK:user_id,Collection.CAFES_PK:cafe_idx},{'_id':False})
    if reviewFlag is not None:
        return Response(status=409)

    today = datetime.now()
    create_date = today.strftime('%Y-%m-%d')
    review_id = DB.allocate_pk(Collection.REVIEWS, Collection.REVIEWS_PK)

    doc = {
        "review_id": review_id,
        "user_id": user_id,
        "cafe_id": cafe_idx,
        "cafe_review": cafe_review,
        "cafe_rating": cafe_rating,
        "create_date": create_date
    }

    DB.insert(Collection.REVIEWS, data=doc)
    return jsonify({'result': 'success'})

