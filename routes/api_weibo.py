import time

from models.comment import Comment
from models.user import User
from routes import current_user, weibo_owner_required, comment_owner_required
from utils import log
from models.weibo import Weibo
from flask import (
    Blueprint,
    request,
    jsonify,
)

api_weibo = Blueprint('api_weibo', __name__)


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据

@api_weibo.route('/api/weibo/all', methods=['GET'])
def weibo_all():
    weibos = Weibo.all_json()
    log('[WEIBO]\n{}'.format(weibos))

    return jsonify(weibos)


@api_weibo.route('/api/comment/all', methods=['GET'])
def comment_all():
    comments = Comment.all_json()
    log('[COMMENTS]\n{}'.format(comments))
    return jsonify(comments)


@api_weibo.route('/api/weibo/add', methods=['POST'])
def add():
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.get_json()
    # 创建一个 weibo
    u = current_user()
    form['user_id'] = u.id
    form['writer'] = u.username
    form['create_time'] = time.time()
    form['update_time'] = form['create_time']
    t = Weibo.new(form)
    # 把创建好的 weibo 返回给浏览器
    return jsonify(t.json())


@api_weibo.route('/api/comment/add', methods=['POST'])
def comment_add():
    form = request.get_json()
    u = current_user()
    t = Comment.add(form, u.id, u.username)
    return jsonify(t.json())


@api_weibo.route('/api/weibo/delete', methods=['GET'])
def delete():
    valid = weibo_owner_required()
    if valid is not None:
        return valid

    weibo_id = int(request.args['id'])
    weibo = Weibo.one(id=weibo_id)
    for i in weibo.comments():
        Comment.delete(i.id)
    Weibo.delete(weibo_id)

    d = dict(
        message="成功删除 weibo"
    )
    return jsonify(d)


@api_weibo.route('/api/comment/delete', methods=['GET'])
def comment_delete():
    valid = comment_owner_required()
    if valid is not None:
        return valid

    comment_id = int(request.args['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 Comment"
    )
    return jsonify(d)


@api_weibo.route('/api/weibo/update', methods=['POST'])
def update():
    """
    用于增加新 weibo 的路由函数
    """
    valid = weibo_owner_required()
    if valid is not None:
        return valid

    form = request.get_json()
    log('api weibo update form', form)
    t = Weibo.update_database(form)
    return jsonify(t.json())


@api_weibo.route('/api/comment/update', methods=['POST'])
def comment_update():
    valid = comment_owner_required()
    if valid is not None:
        return valid

    form = request.json()
    log('api comment update form', form)
    t = Comment.update(form)
    return jsonify(t.json())
