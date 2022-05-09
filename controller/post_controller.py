import jwt
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
# from controller.post_controller import SECRET_KEY
from database import DB
from datetime import datetime

bp = Blueprint('post', __name__)


# 게시판 화면 로드
@bp.route('/post', methods=["GET"])
def board():
    return render_template('userboard_prac.html')

# 게시글 전체 조회
@bp.route('/post/list', methods=["POST"])
def board_listing():
    posts = DB.select_all(collection="posts")
    print(posts)
    return jsonify(posts)

#게시글 등록
@bp.route('/post/', methods=["POST"])
def board_posting():
    post_id = request.form['post_id']
    post_title = request.form['post_title']
    user_nickname = request.form['user_nickname']
    post_view = request.form['post_view']


    doc = {
        'post_id': post_id,
        'post_title': post_title,
        'user_nickname': user_nickname,
        'post_view': post_view,
        'create_date': datetime.now(),
    }
    DB.insert(doc)
    return jsonify({'result': 'success'})