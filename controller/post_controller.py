import jwt
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from controller.auth_controller import SECRET_KEY
from database import DB
from datetime import datetime

bp = Blueprint('post', __name__)


# 게시판 화면 로드
@bp.route('/post', methods=["GET"])
def board():
    token = request.cookies.get("usertoken")
    payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    user = DB.find_one("users", {"user_id": payload["user_id"]})

    return render_template('userBorad.html', user=user)

# 게시글 전체 조회
@bp.route('/post/list', methods=["POST"])
def board_listing():
    posts = DB.find_all_sort(collection="posts")
    for a in posts:

        a['create_date'] = a['create_date'].strftime('%Y.%m.%d')

    return jsonify(posts)

# 게시글 detail 조회
@bp.route('/post/detail', methods=["POST"])
def board_detail_search():
    post_id = int(request.form.get('target_id'))
    DB.update_one("posts", {'post_id': int(post_id)}, {'$inc': {'post_view': 1}})

    article = DB.find_one("posts", {'post_id': int(post_id)})
    article.pop('_id')

    return jsonify({'result': 'success', 'article': article})



#게시글 등록
@bp.route('/post', methods=["POST"])
def board_posting():
    post_title = request.form.get('post_title')
    user_nickname = request.form.get('user_nickname')
    post_content = request.form.get('post_content')
    last_post = DB.idx_plus("posts", "post_id")

    doc = {
        'post_id': last_post,
        'post_title': post_title,
        'post_content': post_content,
        'user_nickname': user_nickname,
        'post_view': 0,
        'create_date': datetime.now(),
    }
    DB.insert("posts", doc)

    return jsonify({'result': 'success'})

#게시글 수정
@bp.route('/post', methods=['PUT'])
def update_article():
    post_id = request.form.get('post_id')
    post_title = request.form.get('post_title')
    post_content = request.form.get('post_content')
    DB.update_one("posts", {'post_id': int(post_id)}, {'$set': {'title': post_title, 'content': post_content}})

    return {"result": "success"}


#게시글 삭제
@bp.route('/post', methods=['DELETE'])
def delete_article():
    post_id = request.args.get('post_id')
    DB.delete("posts", {'post_id': int(post_id)})



    return {"result": "success"}