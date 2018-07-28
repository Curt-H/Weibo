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