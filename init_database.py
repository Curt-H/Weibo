import pymysql
import models.secret as secret


def create_user():
    cmd = 'CRECREATE TABLE IF NOT EXISTS `User`(' \
          '`id` INT AUTO_INCREMENT,' \
          '`user_name` CHAR(32) NOT NULL,' \
          '`password` CHAR(64) NOT NULL,' \
          '`role` CHAR(10) NOT NULL DEFAULT `guest`' \
          'PRIMARY KEY (`id`)' \
          ');'
    return cmd


def creat_session():
    cmd = 'CRECREATE TABLE IF NOT EXISTS `Session`(' \
          '`id` INT AUTO_INCREMENT,' \
          '`session_id` CHAR(36) NOT NULL,' \
          '`user_id` INT NOT NULL,' \
          '`expired_time` INT NOT NULL,' \
          'PRIMARY KEY (`id`)' \
          ');'
    return cmd


def creat_weibo():
    cmd = 'CRECREATE TABLE IF NOT EXISTS `Weibo`(' \
          '`id` INT AUTO_INCREMENT,' \
          '`content` TEXT NOT NULL,' \
          '`user_id` INT NOT NULL,' \
          '`update_time` INT NOT NULL,' \
          '`create_time` INT NOT NULL,' \
          'PRIMARY KEY (`id`)' \
          ');'
    return cmd


def creat_comment():
    cmd = 'CRECREATE TABLE IF NOT EXISTS `Comment`(' \
          '`id` INT AUTO_INCREMENT,' \
          '`content` TEXT NOT NULL,' \
          '`user_id` INT NOT NULL,' \
          '`weibo_id` INT NOT NULL,' \
          '`update_time` INT NOT NULL,' \
          '`create_time` INT NOT NULL,' \
          'PRIMARY KEY (`id`)' \
          ');'
    return cmd


def init_database(db_name, db_pass):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=db_pass,
        db=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    user = create_user()
    session = creat_session()
    weibo = creat_weibo()
    comment = creat_comment()
    with connection.cursor() as cursor:
        cursor.execute(user)
        cursor.execute(session)
        cursor.execute(weibo)
        cursor.execute(comment)
    connection.commit()


if __name__ == '__main__':
    init_database(secret.db_name, secret.db_pass)
