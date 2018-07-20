from flask import Blueprint, render_template
from routes import current_user

# 注册Flask蓝图
public_route = Blueprint('public_route', __name__)


@public_route.route('/', methods=['GET'])
def index():
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user()

    return render_template('index.html', username=u.username)
