from flask import request, jsonify, redirect, url_for

from models.comment import Comment
from models.session import Session
from models.user import User
from models.weibo import Weibo
from utils import log


def current_user():
    """
    获取当前用户的ID信息
    :return: 用户对应的User类
    """
    # 检查cookie里面有没有session_id, 没有则返回游客类
    if 'session_id' in request.cookies:
        # 已知cookie里有session_id, 调取session_id
        session_id = request.cookies['session_id']

        # 在数据库里找到对应的session类
        session = Session.one(session_id=session_id)

        # 找的了Session类则通过里面记录的user id 返回对应的User, 否则反之游客
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
    用于Ajax的错误反馈, 用于权限验证失败的情况, 包括但不限于:
    删除他人的评论, 删除他人的博客
    """
    d = dict(
        error="权限不足"
    )

    return jsonify(d)


def login_required():
    """
    用于验证是否为登陆状态, 不是的话就返回到登陆页面
    """
    log('login_required')
    u = current_user()

    # 如果当前用户是游客就重定向
    if u.is_guest():
        log('游客用户')
        return redirect(url_for('user_route.login_view'))


def weibo_owner_required():
    """
    验证执行操作用户是否是博客的作者
    :return: 不是的话就返回错误信息, 是的话啥都不做
    """
    # 获取当前用户
    u = current_user()
    weibo_id = None

    # 根据不同请求拿这个博客的id
    if request.method == 'GET':
        weibo_id = request.args['id']
    elif request.method == 'POST':
        weibo_id = request.get_json()['id']

    # 验证博客作者id和操作者id是否相同, 不同则报错
    weibo_owner = Weibo.one(id=int(weibo_id)).user_id
    if u.id != weibo_owner:
        return authorize_deny()


def comment_owner_required():
    """
    验证执行操作用户是否是评论的作者
    :return: 验证错误的话返回错误代码
    """
    # 获取当前用户
    u = current_user()
    comment_id = None

    # 根据不同请求拿这个评论的id
    if request.method == 'GET':
        comment_id = request.args['id']
    elif request.method == 'POST':
        comment_id = request.get_json()['id']

    # 验证规则:　只有评论作者和博客作者可以操作
    weibo_id = Comment.find_by(id=int(comment_id)).weibo_id
    weibo_owner = Weibo.one(id=int(weibo_id)).user_id
    comment_owner = Comment.find_by(id=int(comment_id)).user_id

    # 进行验证，失败的话调用错误函数
    if u.id != comment_owner or u.id != weibo_owner:
        return authorize_deny()
