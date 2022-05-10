from flask import Blueprint, jsonify, render_template
from database import DB

bp = Blueprint('cafe', __name__)


@bp.route('/cafe/detail')
def routeCafeDetail():
    return render_template('cafeDetail.html')

@bp.route('/api/cafe/detail/<cafeId>')
def getCafeDetail(cafeId):
    cafe = DB.find_one('cafe', {'cafe_id': cafeId}, {'_id': False})
    events = DB.list('event', {'cafe_id': cafeId}, {'_id': False})
    reviews = []
    for event in events:
        review = DB.list('review', {'event_id': event['event_id']}, {'_id': False})
        reviews.append(review)
    response = {
        'cafe_id': cafe['cafe_id'],
        'cafe_name': cafe['cafe_name'],
        'cafe_info': cafe['cafe_info'],
        'address': cafe['address'],
        'cafe_image': cafe['cafe_image'],
        'x': cafe['x'],
        'y': cafe['y'],
        'reviews': reviews
    }
    return jsonify(response)
