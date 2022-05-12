import datetime
from flask import Blueprint, jsonify, request
from database import DB
from type.collection import Collection

bp = Blueprint('event', __name__)


@bp.route('/api/event/<cafe_id>', methods=['GET'])
def get_event_info(cafe_id):
    year = int(request.args.get('year'));
    month = int(request.args.get('month'));
    events = DB.list(Collection.EVENTS, {Collection.CAFES_PK: int(cafe_id)}, {'_id': False})
    monthEventList = []
    for event in events:
        start_date = event['start_date']
        end_date = event['end_date']
        while start_date <= end_date:
            if start_date.month != month or start_date.year != year:
                break
            monthEventList.append({
                # todo
                # 'event_info': event['event_info'],
                # 'event_name': event['event_name'],
                'event_category': event['event_category'],
                'date': start_date,
            })
            start_date += datetime.timedelta(days=1)
    response = {
        'month_event_list': monthEventList
    }
    return jsonify(response)
