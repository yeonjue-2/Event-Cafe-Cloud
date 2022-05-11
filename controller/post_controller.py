import jwt
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from controller.auth_controller import SECRET_KEY
from database import DB
from datetime import datetime
from type.collection import Collection

from ectoken import ECTOKEN

bp = Blueprint('post', __name__)


# 게시판 화면 로드
@bp.route('/post', methods=["GET"])
def board():
    user = ECTOKEN.get_token()

    return render_template('userBoard.html', user=user)

# 게시글 전체 조회
@bp.route('/api/post', methods=["GET"])
def board_listing():
    posts = DB.find_all_sort(Collection.POSTS)
    for a in posts:

        a['create_date'] = a['create_date'].strftime('%Y.%m.%d')

    return jsonify(posts)

# 게시글 detail 조회
@bp.route('/api/post/detail', methods=["POST"])
def board_detail_search():
    user_id = ECTOKEN.get_user_id()
    post_id = int(request.form.get('target_id'))
    DB.update_one(Collection.POSTS, {'post_id': int(post_id)}, {'$inc': {'post_view': 1}})

    user = DB.find_one(Collection.POSTS, {'post_id': int(post_id)}, {})
    user.pop('_id')
    return jsonify({'result': 'success', 'user': user, 'user_id': user_id})



#게시글 등록
@bp.route('/api/post', methods=["POST"])
def board_posting():
    user = ECTOKEN.get_token()
    if user is not None:
        user_id = user['user_id']
        post_title = request.form.get('post_title')
        post_content = request.form.get('post_content')
        user_nickname = user['user_nickname']
        last_post = DB.sort_post(Collection.POSTS, "post_id")

        doc = {
            'post_id': last_post,
            'post_title': post_title,
            'post_content': post_content,
            'user_id': user_id,
            'user_nickname': user_nickname,
            'post_view': 0,
            'create_date': datetime.now(),
        }
        DB.insert(Collection.POSTS, doc)
        return jsonify({'result': 'success'})

    else:
        return jsonify({'result': 'fail'})



#게시글 수정
@bp.route('/api/post', methods=['PUT'])
def update_post():

    post_id = request.form.get('post_id')
    edit_content = request.form.get('edit_content')

    DB.update_one(Collection.POSTS, {'post_id': int(post_id)}, {'$set': {'post_content': edit_content}})
    return {"result": "success"}


#게시글 삭제
@bp.route('/api/post', methods=['DELETE'])
def delete_post():
    user = ECTOKEN.get_token()
    if user is not None:
        post_id = request.args.get('post_id')
        user_id = DB.find_one(Collection.POSTS, {"post_id": int(post_id)}, {})['user_id']
        deleter = user['user_id']

        if user_id == deleter:
            DB.delete(Collection.POSTS, {'post_id': int(post_id)})
            return {"result": "success"}
        else:
            return {"result": "fail"}
    else:
        return {"result": "notlogined"}


