import pymysql
import models.secret as secret
from utils import log


class SQLModel(object):
    # 链接数据库
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=secret.db_pass,
        db=secret.db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        """
        :return: 将类的名字作为数据库的表格名
        """
        return '`{}`'.format(cls.__name__)

    @classmethod
    def new(cls, form):
        """
        用于新建一个model类
        :param form: form是包含所需元素的字典
        :return: 返回创建的一个对象
        """
        m = cls(form)
        cls_id = cls.insert(m.__dict__)
        m.id = cls_id
        return m

    @classmethod
    def insert(cls, form):
        """
        插入数据的方法
        :param form: form是包含数据表的每个单元的数据的字典
        :return: 返回由数据库的对象的id
        """
        # 把id删掉
        log(form)
        form.pop('id')

        # 将字典的键值分开, 并预先拼好语句
        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_values = ', '.join(['%s'] * len(form))
        sql_insert = 'INSERT INTO \n\t{} ({}) \nVALUES \n\t({})'.format(
            cls.table_name(),
            sql_keys,
            sql_values,
        )
        log(sql_insert)
        values = tuple(form.values())

        # 启动cursor, 开始发起
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            # 获取最后一行的id作为新数据的id
            _id = cursor.lastrowid
        # 提交变更
        cls.connection.commit()

        return _id

    @classmethod
    def delete(cls, id):
        """
        删除id对应的数据行
        :param id: 数据id
        """
        sql_delete = 'DELETE FROM {} WHERE `id`=%s'.format(cls.table_name())
        log(sql_delete)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (id,))
        cls.connection.commit()

    @classmethod
    def update(cls, id, **kwargs):
        """
        更新数据
        :param id: 对象的id
        :param kwargs: 需要被更新的键值对
        :return: 返回更新后的对象
        """
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
        """
        获取所有的数据
        :return: 包含所有model的list
        """
        # SELECT * FROM User
        sql_select = 'SELECT * FROM \n\t{}'.format(cls.table_name())
        log(sql_select)

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
        """
        查找符合特定条件的第一个对象
        :param kwargs: 条件
        :return: 被查到的对象
        """
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

    @classmethod
    def all_by(cls, **kwargs):
        """
        查找符合特定条件的所有对象
        :param kwargs: 条件
        :return: 被查到的对象list
        """
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

        ms = list()
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchall()
            for r in result:
                m = cls(r)
                ms.append(m)
            return ms

    def json(self):
        return self.__dict__

    @classmethod
    def all_json(cls):
        """
        用于将所有对象转换成JSON格式
        :return:　JSON格式的对象
        """
        items = cls.all()
        # 要转换为 dict 格式才行
        js = [t.json() for t in items]
        return js

    def __repr__(self):
        name = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(name, s)
