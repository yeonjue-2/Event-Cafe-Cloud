import jwt
from flask import request, render_template, Blueprint

from database import DB
from controller.auth_controller import SECRET_KEY
from ectoekn import ECTOKEN

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
    user = ECTOKEN.get_token(object)
    if user is not None:
        return render_template('index.html', user=user)
    else:
        return render_template('index.html', msg="로그인 정보가 없습니다")

