from models import Model
from models.user import User


# from models.weibo import Weibo


class Comment(Model):
    """
    评论类
    """

    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))
        self.username = form.get('username', None)

    @classmethod
    def add(cls, form, user_id, username):
        w = Comment(form)
        w.user_id = user_id
        w.username = username
        w.save()
        return w

    @classmethod
    def update(cls, form):
        comment_id = int(form['id'])
        w = Comment.find_by(id=comment_id)
        w.content = form['content']
        w.save()
        return w

    def user(self):
        u = User.one(id=self.user_id)
        return u

    # def weibo(self):
    #     w = Weibo.find_by(id=self.weibo_id)
    #     return w
