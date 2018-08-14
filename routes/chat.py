from flask import (
    Blueprint,
    render_template,
)

from routes import current_user

chats = Blueprint('chatroom', __name__)


@chats.route('/chatroom')
def chat():
    u = current_user()
    return render_template('chatroom.html', u=u)
