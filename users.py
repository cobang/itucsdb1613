import pymysql
from dbconnection import MySQL


class Users:
    def __init__(self):
        self.users = {}
        self.key = 0

    def add_user(self, user):
        self.key += 1
        #user.key = self.key
        self.users[self.key] = user

    def get_user(self, key):
        return self.users[key]

    def get_users(self):
        return sorted(self.users.items())


class User:
    def __init__(self, user_id, user_type, user_email=" ", user_password=" "):
        self.user_id = user_id
        self.user_type = user_type
        self.user_email = user_email
        self.user_password = user_password


def user_list():
    store = Users()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT user_id, user_type, user_email, user_password FROM users"""

        c.execute(sql)

        for row in c:
            user_id, user_type, user_email, user_password = row
            user = User(user_id=user_id, user_type=user_type, user_email=user_email, user_password=user_password)
            store.add_user(user=user)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    return store.get_users()


def user_edit(user_id, user_name, user_surname):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """UPDATE users SET user_name = '%s', user_surname = '%s'  WHERE user_id = %d """ % (
            user_name, user_surname, int(user_id))

        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def user_delete(user_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """DELETE FROM users WHERE user_id = (%d) """ % (int(user_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))
