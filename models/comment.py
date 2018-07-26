import time

from models.base_model import SQLModel

# from models.weibo import Weibo
from models.user import User
from models.weibo import Weibo


class Comment(SQLModel):
    """
    评论类
    """

    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))
        self.writer = self.get_writer()
        self.weibo_writer = self.get_weibo_writer()
        self.update_time = form.get('update_time', int(time.time()))
        self.create_time = form.get('create_time', int(time.time()))

    def get_writer(self):
        return User.one(id=self.user_id).username

    def get_weibo_writer(self):
        return Weibo.one(id=self.weibo_id).user_id
