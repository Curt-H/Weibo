import random

from flask import request, jsonify, redirect, url_for

from models.comment import Comment
from models.session import Session
from models.user import User
from models.weibo import Weibo
from utils import log


def random_string():
    """
    生成一个随机的字符串
    """
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        # 这里 len(seed) - 2 是因为我懒得去翻文档来确定边界了
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user():
    if 'session_id' in request.cookies:
        session_id = request.cookies.get('session_id', 'guest')
        session = Session.one(session_id=session_id)
        if session is not None:
            user_id = session.user_id
            user = User.one(id=user_id)
            return user
        else:
            return User.guest()
    else:
        return User.guest()


def authorize_deny():
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    d = dict(
        error="权限不足"
    )
    return jsonify(d)


def login_required():
    """
    这个函数看起来非常绕，所以你不懂也没关系
    就直接拿来复制粘贴就好了
    """

    log('login_required')
    u = current_user()
    if u.is_guest():
        log('游客用户')
        return redirect(url_for('user_route.login_view'))


def weibo_owner_required():
    u = current_user()
    weibo_id = None
    if request.method == 'GET':
        weibo_id = request.args['id']
    elif request.method == 'POST':
        weibo_id = request.get_json()['id']
    weibo_owner = Weibo.one(id=int(weibo_id)).user_id
    if u.id != weibo_owner:
        return authorize_deny()


def comment_owner_required():
    u = current_user()
    comment_id = None
    if request.method == 'GET':
        comment_id = request.args['id']
    elif request.method == 'POST':
        comment_id = request.get_json()['id']

    weibo_id = Comment.find_by(id=int(comment_id)).weibo_id
    weibo_owner = Weibo.one(id=int(weibo_id)).user_id

    comment_owner = Comment.find_by(id=int(comment_id)).user_id
    if u.id != comment_owner or u.id != weibo_owner:
        return authorize_deny()
