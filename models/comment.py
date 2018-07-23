from models.user import User
from models.base_model import SQLModel


# from models.weibo import Weibo


class Comment(SQLModel):
    """
    评论类
    """

    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))
        self.username = form.get('username', None)
