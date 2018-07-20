import pymysql

from models.secret import db_name, mysql_password
from utils import log


class SQLModel(object):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=mysql_password,
        db=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__)

    @classmethod
    def new(cls, form):
        # cls(form) 相当于 User(form)
        m = cls(form)
        cls_id = cls.insert(m.__dict__)
        m.id = cls_id
        return m

    @classmethod
    def insert(cls, form):
        form.pop('id')
        # INSERT INTO `User` (
        #   `username`, `password`, `email`
        # ) VALUES (
        #   'xx', 'xxx', 'xxx'
        # )
        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_values = ', '.join(['%s'] * len(form))
        sql_insert = 'INSERT INTO \n\t{} ({}) \nVALUES \n\t({})'.format(
            cls.table_name(),
            sql_keys,
            sql_values,
        )
        print(sql_insert)

        values = tuple(form.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()

        return _id

    @classmethod
    def delete(cls, id):
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())
        print(sql_delete)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (id,))
        cls.connection.commit()

    @classmethod
    def update(cls, id, **kwargs):
        # UPDATE
        # 	`User`
        # SET
        # 	`username`='test', `password`='456'
        # WHERE `id`=3;
        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = 'UPDATE \n\t{} \nSET \n\t{} \nWHERE `id`=%s'.format(
            cls.table_name(),
            sql_set,
        )
        print(sql_update)

        values = list(kwargs.values())
        values.append(id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

        updated_data = cls.one(id=id)
        return updated_data

    @classmethod
    def all(cls):
        # SELECT * FROM User
        sql_select = 'SELECT * FROM \n\t{}'.format(cls.table_name())

        print(sql_select)

        ms = []
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select)
            result = cursor.fetchall()
            for row in result:
                m = cls(row)
                ms.append(m)
            return ms

    @classmethod
    def one(cls, **kwargs):
        sql_select = 'SELECT * FROM \n' \
                     '\t{} \n' \
                     'WHERE \n' \
                     '\t{}\n' \
                     'LIMIT 1'
        sql_keys = ' AND '.join(['`{}`=%s'.format(k) for k in kwargs.keys()])
        sql_select = sql_select.format(
            cls.table_name(),
            sql_keys
        )
        log('SQL Sentence:\n{}'.format(sql_select))

        values = tuple(kwargs.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchone()
            if result is None:
                return None
            else:
                return cls(result)

    def json(self):
        return self.__dict__

    @classmethod
    def all_json(cls):
        items = cls.all()
        # 要转换为 dict 格式才行
        js = [t.json() for t in items]
        return js

    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        不明白就看书或者 搜
        """
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)

# class SimpleUser(SQLModel):
#     sql_create = '''
#     CREATE TABLE `simpleuser` (
#         `id` INT NOT NULL AUTO_INCREMENT,
#         `username` VARCHAR(45) NOT NULL,
#         `password` CHAR(3) NOT NULL,
#         `email` VARCHAR(45) NOT NULL,
#         PRIMARY KEY (`id`)
#     )'''
#
#     def __init__(self, form):
#         super().__init__(form)
#         self.username = form['username']
#         self.password = form['password']
#         self.email = form['email']
#
#
# def recreate_database():
#     connection = pymysql.connect(
#         host='localhost',
#         user='root',
#         password=secret.mysql_password,
#         charset='utf8mb4',
#         cursorclass=pymysql.cursors.DictCursor
#     )
#
#     with connection.cursor() as cursor:
#         cursor.execute(
#             'DROP DATABASE IF EXISTS `{}`'.format(
#                 db_name
#             )
#         )
#         cursor.execute(
#             'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
#                 db_name
#             )
#         )
#         cursor.execute('USE `{}`'.format(db_name))
#         cursor.execute(SimpleUser.sql_create)
#
#     connection.commit()
#     connection.close()
#
#
# def test():
#     f = dict(
#         username='456',
#         password='789',
#         email='test',
#     )
#     u = SimpleUser.new(f)
#     print('User.new <{}>'.format(u))
#     assert u.username == '456'
#
#     us = SimpleUser.all()
#     print('User.all <{}>'.format(us))
#     assert len(us) >= 0
#
#     u = SimpleUser.one_for_username_and_password(username='456', password='789')
#     print('User.one <{}>'.format(u))
#     assert u.username == '456'
#
#     SimpleUser.update(u.id, username='456', email='789')
#     u = SimpleUser.one_for_username_and_password(username='456', password='789')
#     print('User.one <{}>'.format(u))
#     assert u.username == '456'
#
#     SimpleUser.delete(u.id)
#     u = SimpleUser.one_for_username_and_password(username='456', password='123')
#     print('User.one <{}>'.format(u))
#     assert u is None
#
#
# if __name__ == '__main__':
#     recreate_database()
#     test()
