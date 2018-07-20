sfrom flask import Flask
from utils import log
from routes.routes_public import public_route as public
from routes.routes_todo import todo_route as todo
from routes.routes_weibo import weibo_route as weibo
from routes.api_weibo import api_weibo
from routes.routes_user import user_route


def configured_app():
    server = Flask(__name__)
    server.register_blueprint(public)
    server.register_blueprint(todo)
    server.register_blueprint(weibo)
    server.register_blueprint(api_weibo)
    server.register_blueprint(user_route)
    log('URL MAP\n'.format(server.url_map))
    return server


if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    # app = Flask(__name__)
    # register_route(app)
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=80,
    )
    app.run(**config)
