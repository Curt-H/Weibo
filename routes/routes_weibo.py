from models.weibo import Weibo
from flask import Blueprint, render_template, redirect, url_for

from routes import current_user, login_required
from utils import log

weibo_route = Blueprint('weibo_route', __name__)


@weibo_route.route('/weibo/index', methods=['GET'])
def index():
    """
    weibo 首页的路由函数
    """
    valid = login_required()
    if valid is not None:
        return valid
    u = current_user()
    weibos = Weibo.one(user_id=u.id)
    # 替换模板文件中的标记字符串
    return render_template('weibo_index.html', weibos=weibos, user=u)
