from flask import Flask
from utils import log

# 路由函数包导入
from routes.routes_public import public_route as public
from routes.routes_weibo import weibo_route as weibo
from routes.api_weibo import api_weibo
from routes.routes_user import user_route
from routes.chat import chats
from events import socketio


def configured_app():
    """
    app配置函数, 用于配置Flask主程序的路由蓝图, 数据库等
    :return: app                                      N
    """
    server = Flask(__name__)

    # 注册路由蓝图
    server.register_blueprint(public)
    server.register_blueprint(weibo)
    server.register_blueprint(api_weibo)
    server.register_blueprint(user_route)
    server.register_blueprint(chats)
    socketio.init_app(server)

    return server


if __name__ == '__main__':
    app = configured_app()

    # Flask运行参数配置, 正式执行时必须要关闭debug模式
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=80,
    )

    socketio.run(app, **config)
