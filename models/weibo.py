from models.base_model import SQLModel
from models.comment import Comment


class Weibo(SQLModel):
    """
    微博类
    """

    def __init__(self, form):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', None)
        self.username = form.get('username', None)

    @classmethod
    def update_database(cls, form):
        weibo_id = form['id']
        form.pop('id')
        cls.update(weibo_id, **form)
        return cls.one(id=weibo_id)

    def comments(self):
        cs = Comment.all(weibo_id=self.id)
        return cs
