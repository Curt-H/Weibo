import time

from models.comment import Comment
from routes import current_user
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


@api_weibo.route('/api/weibo/add', methods=['POST'])
def weibo_add():
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


@api_weibo.route('/api/weibo/delete', methods=['GET'])
def weibo_delete():
    # 获取微博的ID
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    weibo_id = request.args['id']
    log(f'{weibo_id} -- {type(weibo_id)}')
    # 验证数据是否是数字
    valid = weibo_id
    for i in range(len(valid)):
        if valid[i] not in numbers:
            log(f'获取数据错误, 获取到非数字<{valid[i]}>, <{i}> of <{weibo_id}>')
            r = dict(
                message='DataError'
            )
            return jsonify(r)
    weibo_id = int(weibo_id)

    weibo = Weibo.one(id=weibo_id)
    for i in weibo.comments():
        Comment.delete(i.id)
    Weibo.delete(weibo_id)

    d = dict(
        message="成功删除 weibo"
    )
    return jsonify(d)


@api_weibo.route('/api/weibo/update', methods=['POST'])
def weibo_update():
    """
    用于增加新 weibo 的路由函数
    """
    form = request.get_json()
    form['update_time'] = int(time.time())
    log('api weibo update form', form)
    t = Weibo.update_database(form)
    return jsonify(t.json())


@api_weibo.route('/api/comment/all', methods=['GET'])
def comment_all():
    comments = Comment.all_json()
    log('[COMMENTS]\n{}'.format(comments))
    return jsonify(comments)


@api_weibo.route('/api/comment/add', methods=['POST'])
def comment_add():
    """
    用于向数据库添加评论数据
    :return:
    """
    form = request.get_json()

    u = current_user()
    form['user_id'] = u.id
    form['writer'] = u.username
    form['create_time'] = int(time.time())
    form['update_time'] = form['create_time']

    t = Comment.new(form)

    return jsonify(t.json())


@api_weibo.route('/api/comment/delete', methods=['GET'])
def comment_delete():
    comment_id = int(request.args['id'])
    Comment.delete(comment_id)
    d = dict(
        message="成功删除 Comment"
    )
    return jsonify(d)


@api_weibo.route('/api/comment/update', methods=['POST'])
def comment_update():
    form = request.get_json()
    form['update_time'] = int(time.time())

    log('api comment update form', form)
    t = Comment.update_comment(form)
    return jsonify(t.json())
