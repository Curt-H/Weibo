import time
from models.base_model import SQLModel
from utils import log


class Session(SQLModel):
    # TODO(Curt): 考虑Session的处理, 当处于已登录状态时再次登录其他账号失败时, 应删除Session
    # TODO(Curt): 同一账号不同时间登录时, Session应该为更新而不是删除
    """
    Session 是用来保存 session 的 model
    """

    def __init__(self, form):
        super().__init__(form)
        self.session_id = form.get('session_id', '')
        self.user_id = form.get('user_id', -1)
        self.expired_time = form.get('expired_time', time.time() + 3600)

    def expired(self):
        now = time.time()
        result = self.expired_time < now
        log('expired', result, self.expired_time, now)
        return result
