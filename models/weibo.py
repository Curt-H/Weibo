import time

from models.base_model import SQLModel
from models.comment import Comment
from models.user import User
from utils import log


class Weibo(SQLModel):
    """
    微博类
    """

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)
        self.writer = self.get_writer()
        self.update_time = form.get('update_time', int(time.time()))
        self.create_time = form.get('create_time', int(time.time()))

    @classmethod
    def update_database(cls, form):
        weibo_id = form['id']
        form.pop('id')
        cls.update(weibo_id, **form)
        return cls.one(id=weibo_id)

    def comments(self):
        cs = Comment.all_by(weibo_id=self.id)
        return cs

    def get_writer(self):
        log(f'用户的id: {self.user_id}|<{type(self.user_id)}>')
        username = User.one(id=self.user_id).username
        return username
