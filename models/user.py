from models.base_model import SQLModel
from models.user_role import UserRole
import hashlib
from utils import log


class User(SQLModel):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    def __init__(self, form):
        super().__init__(form)
        self.username = form['username']
        self.password = form['password']
        self.role = form.get('role', UserRole.normal)

    @staticmethod
    def guest():
        """
        创建一个游客用户
        :return: 返回一个游客用户实例
        """

        form = dict(
            role=UserRole.guest,
            username='【游客】',
            id=-1,
            password='guest'
        )
        u = User(form)
        return u

    def is_guest(self):
        """
        判断实例的身份是否是游客
        :return: 返回布尔值
        """
        return self.role == UserRole.guest

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        """
        对密码进行加盐, 并求hash
        :param password: 密码
        :param salt: 盐
        :return: 返回加盐后的密码摘要
        """
        salted = password + salt
        hash_password = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash_password

    @classmethod
    def login(cls, form):
        """
        进行登录信息判断
        :param form: 登录信息
        :return: 登录成功则返回用户和成功信息, 否则返回游客实例和错误信息
        """
        salted = cls.salted_password(form.get('password', ''))
        u = User.one(username=form['username'], password=salted)
        if u is not None:
            result = '登录成功'
            return u, result
        else:
            result = '用户名或者密码错误'
            return User.guest(), result

    @classmethod
    def register(cls, form):
        """
        用于注册新用户
        :param form: 新用户的信息
        :return: 用户实例和提示信息
        """
        # 判断密码是否合规
        valid = len(form['username']) > 2 and len(form['password']) > 2
        log(form['username'], form['password'])

        # 不合规则返回成游客用户
        if valid:
            form['password'] = cls.salted_password(form['password'])
            u = User.new(form)
            result = '注册成功'
            return u, result
        else:
            result = '用户名或者密码长度必须大于2'
            return User.guest(), result
