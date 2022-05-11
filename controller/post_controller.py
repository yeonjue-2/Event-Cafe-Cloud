import jwt
from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from controller.auth_controller import SECRET_KEY
from database import DB
from datetime import datetime

from ectoekn import ECTOKEN

bp = Blueprint('post', __name__)


# 게시판 화면 로드
@bp.route('/post', methods=["GET"])
def board():
    user = ECTOKEN.get_token(object)

    return render_template('userBoard.html', user=user)

# 게시글 전체 조회
@bp.route('/api/post', methods=["GET"])
def board_listing():
    posts = DB.find_all_sort(collection="posts")
    for a in posts:

        a['create_date'] = a['create_date'].strftime('%Y.%m.%d')

    return jsonify(posts)

# 게시글 detail 조회
@bp.route('/api/post/detail', methods=["POST"])
def board_detail_search():
    user_id = ECTOKEN.get_user_id(object)
    post_num = int(request.form.get('target_id'))
    DB.update_one("posts", {'post_num': int(post_num)}, {'$inc': {'post_view': 1}})

    user = DB.find_one("posts", {'post_num': int(post_num)}, {})
    user.pop('_id')
    return jsonify({'result': 'success', 'user': user, 'user_id': user_id})



#게시글 등록
@bp.route('/api/post', methods=["POST"])
def board_posting():
    user = ECTOKEN.get_token(object)
    if user is not None:
        user_id = user['user_id']
        post_title = request.form.get('post_title')
        post_content = request.form.get('post_content')
        user_nickname = user['user_nickname']
        last_post = DB.sort_post("posts", "post_num")

        doc = {
            'post_num': last_post,
            'post_title': post_title,
            'post_content': post_content,
            'user_id': user_id,
            'user_nickname': user_nickname,
            'post_view': 0,
            'create_date': datetime.now(),
        }
        DB.insert("posts", doc)
        return jsonify({'result': 'success'})

    else:
        return jsonify({'result': 'fail'})



#게시글 수정
@bp.route('/api/post', methods=['PUT'])
def update_post():

    post_num = request.form.get('post_num')
    edit_content = request.form.get('edit_content')

    DB.update_one("posts", {'post_num': int(post_num)}, {'$set': {'post_content': edit_content}})
    return {"result": "success"}


#게시글 삭제
@bp.route('/api/post', methods=['DELETE'])
def delete_post():
    user = ECTOKEN.get_token(object)
    if user is not None:
        post_num = request.args.get('post_num')
        user_id = DB.find_one("posts", {"post_num": int(post_num)}, {})['user_id']
        deleter = user['user_id']

        if user_id == deleter:
            DB.delete("posts", {'post_num': int(post_num)})
            return {"result": "success"}
        else:
            return {"result": "fail"}
    else:
        return {"result": "notlogined"}


