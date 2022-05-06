import jwt
from flask import request, render_template, Blueprint

from database import DB
from views.auth_views import SECRET_KEY

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    token = request.cookies.get("usertoken")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = DB.find_one("users", {"user_id": payload["user_id"]})
        print(user)
        return render_template('index.html', user=user)
    except jwt.ExpiredSignatureError:
        return render_template('index.html', msg="로그인 시간이 만료되었습니다.")
    except jwt.exceptions.DecodeError:
        return render_template('index.html', msg="로그인 정보가 없습니다!")