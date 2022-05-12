import datetime
from flask import Blueprint, jsonify, request
from database import DB
from type.collection import Collection

bp = Blueprint('event', __name__)


@bp.route('/api/event/<cafe_id>', methods=['GET'])
def get_schedule_info(cafe_id):
    year = int(request.args.get('year'));
    month = int(request.args.get('month'));
    events = DB.list(Collection.EVENTS, {Collection.CAFES_PK: int(cafe_id)}, {'_id': False})

    monthEventList = []
    for event in events:
        start_date = event['event_start_date']
        end_date = event['event_end_date']
        while start_date <= end_date:
            if start_date.month != month or start_date.year != year:
                break
            monthEventList.append({
                'event_info': event['event_info'],
                'event_name': event['event_name'],
                'event_category': event['event_category'],
                'date': start_date,
            })
            start_date += datetime.timedelta(days=1)

    customs = DB.list(Collection.CUSTOMS, {Collection.CAFES_PK: cafe_id}, {'_id': False})

    monthCustomList = []
    for custom in customs:
        start_date = datetime.datetime.strptime(custom['custom_start_date'],'%Y-%m-%d')
        end_date = datetime.datetime.strptime(custom['custom_end_date'],'%Y-%m-%d')
        while start_date <= end_date:
            if start_date.month != month or start_date.year != year:
                break
            monthCustomList.append({
                'custom_name': custom['custom_name'],
                'custom_sales_flag': custom['custom_sales_flag'],
                'date': start_date,
            })
            start_date += datetime.timedelta(days=1)
    response = {
        'month_event_list': monthEventList,
        'month_custom_list':monthCustomList
    }
    return jsonify(response)
