from datetime import datetime, timedelta

from flask import Blueprint, jsonify, render_template, request, Response
from database import DB
from ectoken import ECTOKEN
from type.collection import Collection

bp = Blueprint('cafe', __name__)


@bp.route('/cafe/detail')
def routeCafeDetail():
    cafe_id = int(request.args.get('id'));
    user = ECTOKEN.get_token();
    if DB.find_one(Collection.CAFES, {Collection.CAFES_PK: cafe_id}, {'_id': False}) is None:
        return Response(status=404)
    if user is None:
        return render_template('cafeDetail.html', msg="로그인 정보가 없습니다")
    return render_template('cafeDetail.html', user=user)


@bp.route('/cafe/eventRegister')
def routeEventRegister():
    user = ECTOKEN.get_token()
    if user is None:
        return render_template('cafeDetail.html', msg="로그인 정보가 없습니다")
    return render_template('regEvent.html', user=user)


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

    reviewFlag = DB.find_one(Collection.REVIEWS, {Collection.USERS_PK: user_id, Collection.CAFES_PK: cafe_idx},
                             {'_id': False})
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


def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [(start + timedelta(days=i)) for i in range((end - start).days + 1)]
    return dates


def getCostByDay(custom_days, event_day, holiday_cost, weekday_cost):
    try:
        return int(custom_days[event_day])
    except KeyError:
        if event_day.weekday() == 5 or event_day.weekday() == 6:
            return int(holiday_cost)
        else:
            return int(weekday_cost)


@bp.route('/api/cafe/costByDate', methods=["GET"])
def countCostByDate():
    cafe_id = request.args.get('cafe_id')
    cafe = DB.find_one(Collection.CAFES, {Collection.CAFES_PK: int(cafe_id)}, {'_id': False})

    all_cost = 0

    # 카페 기본 가격
    weekday_cost = cafe['cafe_default_cost_weekday']
    holiday_cost = cafe['cafe_default_cost_holiday']

    # [event_days]에 시작과 종료일 사이 기간을 저장
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    event_days = date_range(start_date, end_date)

    # 카페에서 설정한 날짜에 따른 가격을 따로 호출
    customs = DB.list(Collection.CUSTOMS, {Collection.CAFES_PK: cafe_id}, {'_id': False})
    custom_dict = {}

    # custom 시작과 종료일에 따른 가격과 각각의 날짜를 딕셔너리 형태로 custom_dict에 저장
    for custom in customs:
        custom_start_date = custom['custom_start_date']
        custom_end_date = custom['custom_end_date']
        custom_cost = custom['custom_cost']

        while custom_start_date <= custom_end_date:
            date = custom_start_date
            custom_dict[date] = custom_cost
            custom_start_date += timedelta(days=1)

    for event_day in event_days:
        temp_cost = getCostByDay(custom_dict, event_day, holiday_cost, weekday_cost)
        all_cost += temp_cost

    return jsonify({"result": "success", "all_cost": all_cost})


@bp.route('/api/cafe/registerEvent', methods=["POST"])
def regEvent():
    user_id = ECTOKEN.get_user_id()
    cafe_id = request.form['cafe_id']
    event_category = request.form['event_category']
    event_name = request.form['event_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    event_cost = request.form['event_cost']

    event_id = DB.allocate_pk(Collection.EVENTS, Collection.EVENTS_PK)
    event_start_date = datetime.strptime(start_date, '%Y-%m-%d')
    event_end_date = datetime.strptime(end_date, '%Y-%m-%d')

    doc = {
        Collection.EVENTS_PK: event_id,
        Collection.USERS_PK: user_id,
        Collection.CAFES_PK: cafe_id,
        'event_category': event_category,
        'event_name': event_name,
        'event_start_date': event_start_date,
        'event_end_date': event_end_date,
        'event_cost': event_cost,
    }

    DB.insert(Collection.EVENTS, data=doc)
    return jsonify({'result': 'success'})
