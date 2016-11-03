import pymysql
from dbconnection import MySQL

class Connection:
    def __init__(self, user_id, following_id, date):
        self.user = user_id
        self.following = following_id
        self.date = date
        self.added_to_favorites = 0
    def get_name(self):
        try:
            user_name=" "
            user_surname = " "
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT * FROM users WHERE user_id = (%d)""" % (int(self.following))
            c.execute(sql)
            for row in c:
                user_id, user_name, user_surname, user_email, user_password = row
                print("df")
                print(user_name)
                print("df")
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))
        return user_name + " " + user_surname


    def get_email(self):
        try:
            user_email = " "
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT * FROM users WHERE user_id = (%d)""" % (int(self.following))
            c.execute(sql)
            for row in c:
                user_id, user_name, user_surname, user_email, user_password = row
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))
        return user_email


class Connections:
    def __init__(self):
        self.connections = {}
        self.recommendations = {}
        self.counter = 0

    def add_connection(self, connection):
        self.counter += 1
        self.connections[self.counter] = connection

    def delete_connection(self, counter):
        del self.connections[counter]
        self.counter -= 1

    def get_connection(self, counter):
        return self.connections[counter]

    def get_connections(self):
        return self.connections.items()


class Recommendations:
    def __init__(self):
        self.recommendations = {}
        self.key = 0
        self.get=0

    def add_recommendation(self, connection):
        self.key += 1
        self.recommendations[self.key] = connection

    def delete_recommendation(self, key):
        print(key)
        del self.recommendations[key]
        self.key -= 1

    def delet_byid(self, id):
        for c in self.recommendations:
            if id == self.get_recommendation(c).following:
                self.delete_recommendation(c)

    def is_item(self, id):
        for c in self.recommendations:
            if id == self.get_recommendation(c).following:
                return 0
        return 1
    def get_recommendation(self, key):
        return self.recommendations[key]

    def get_recommendations(self):
        return self.recommendations.items()


def connection_add(u_id, fol_id, time):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        f = '%Y-%m-%d %H:%M:%S'
        c = conn.cursor()
        sql = """INSERT INTO connections(user_id,following_id,connection_date)
                              VALUES (%d, '%d', '%s' )""" % (u_id, fol_id, time.strftime(f))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()
    except Exception as e:
        print(str(e))

def connection_remove(u_id, fol_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        print(fol_id)
        sql = """DELETE FROM connections WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()
        print("afterdelete")

    except Exception as e:
        print(str(e))

def add_to_favorites (u_id, fol_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """UPDATE connections
                  SET added_to_favorites = 1
                  WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

