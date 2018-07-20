from models.session import Session
from routes import current_user
from utils import log
from models.user import User
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    make_response)
import uuid

user_route = Blueprint('user_route', __name__)


@user_route.route('/user/login', methods=['POST'])
def login():
    """
    登录页面的路由函数
    """
    form = request.form
    log('FORM\n{}'.format(form))

    session_id = None
    u, result = User.login(form)
    if not u.is_guest():
        # session ID的生成使用uuid的伪随机字符串生成器
        session_id = str(uuid.uuid4())

        form = dict(
            session_id=session_id,
            user_id=u.id,
        )
        Session.new(form)
    log('USER\n{}'.format(u.username))
    # cookie 范围
    # /login
    # /login/user/view
    # /todo
    response = make_response(render_template('login.html', username=u.username, result=result))
    if session_id is not None:
        response.set_cookie('session_id', session_id)
    return response


@user_route.route('/user/login/view', methods=['GET'])
def login_view():
    u = current_user()
    return render_template('login.html', username=u.username)


@user_route.route('/user/register', methods=['POST'])
def register():
    """
    注册页面的路由函数
    """
    form = dict()
    for k in request.form:
        form[k] = ''.join(request.form[k])

    u, result = User.register(form)
    log('register post', result)

    return redirect(url_for('user_route.register_view', result=result))


@user_route.route('/user/register/view', methods=['GET'])
def register_view():
    result = request.args.get('result', '')

    return render_template('register.html', result=result)


# RESTFul
# GET /login
# POST /login
# UPDATE /user
# DELETE /user
#

def route_dict():
    r = {
        '/user/login': login,
        '/user/login/view': login_view,
        '/user/register': register,
        '/user/register/view': register_view,
    }
    return r
