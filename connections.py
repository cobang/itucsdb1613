import pymysql
import datetime
from dbconnection import MySQL

class Connection:
    def __init__(self, user_id, following_id, fav, date):
        self.user = user_id
        self.following = following_id
        self.date = date
        self.added_to_favorites = fav

    def get_name(self):
        try:
            name = ""
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT user_type, user_id FROM users WHERE user_id = (%d)""" % (int(self.following))
            c.execute(sql)
            for row in c:
                user_type, user_id = row

            if user_type == 1:
                sql = """SELECT user_name,user_surname FROM user_detail WHERE user_id = (%d)""" % (int(self.following))
                c.execute(sql)
                for row in c:
                    user_name, user_surname = row
                name = user_name + " " + user_surname

            elif user_type == 2:
                sql = """SELECT company_name, user_id FROM company_detail WHERE user_id = (%d)""" % (int(self.following))
                c.execute(sql)
                for row in c:
                    company_name, user_id = row
                name = company_name
            else:
                sql = """SELECT university_name, user_id FROM university_detail WHERE user_id = (%d)""" % (int(self.following))
                c.execute(sql)
                for row in c:
                    university_name, user_id = row
                name = university_name
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))
        return name

    def get_detail(self):
        try:
            detail = ""
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT user_type, user_id FROM users WHERE user_id = (%d)""" % (int(self.following))
            c.execute(sql)
            for row in c:
                user_type, user_id = row

            if user_type == 1:
                sql = """SELECT user_name,address FROM user_detail WHERE user_id = (%d)""" % (int(self.following))
                c.execute(sql)
                for row in c:
                    user_name, address = row
                detail = address

            elif user_type == 2:
                sql = """SELECT company_name, company_address FROM company_detail WHERE user_id = (%d)""" % (int(self.following))
                c.execute(sql)
                for row in c:
                    company_name, company_address = row
                detail = company_address
            else:
                sql = """SELECT university_address, user_id FROM university_detail WHERE user_id = (%d)""" % (int(self.following))
                c.execute(sql)
                for row in c:
                    university_address, user_id = row
                detail = university_address
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))
        return detail


    def get_num_of_connections(self):

        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT num_of_connections,user_id FROM connections_detail WHERE user_id = (%d)""" % (int(self.following))
        c.execute(sql)
        for row in c:
            numC, user_id = row
        c.close()
        conn.close()
        print("mal")
        return numC

    def get_email(self):
        try:
            user_email=""
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT user_email, user_id FROM users WHERE user_id = (%d)""" % (int(self.following))
            c.execute(sql)
            for row in c:
                user_email, user_id = row
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))
        return user_email


class Connections:
    def __init__(self):
        self.connections = {}
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

    def add_forhtml(self,id):
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """SELECT following_id, user_id FROM connections WHERE user_id = (%d)""" % (int(id))
        c.execute(sql)
        for row in c:
            following_id, user_id =row
            connection_new = Connection(id, following_id=user_id, fav=0, date=0)
            self.add_connection(connection_new)
        c.close()
        conn.close()
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


def recommendation_add(u_id, fol_id):
    try:
        print("add to rec table")
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """INSERT INTO recommended(following_id,user_id)
                              VALUES (%d, '%d' )""" % (fol_id,u_id)
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()
    except Exception as e:
        print(str(e))

def recommendation_remove(u_id, fol_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        print(fol_id)
        sql = """DELETE FROM recommended WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
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


def remove_from_favorites (u_id, fol_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """UPDATE connections
                  SET added_to_favorites = 0
                  WHERE user_id = (%d) AND  following_id = (%d)""" % (int(u_id), int(fol_id))
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

def num():
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """SELECT COUNT(*) FROM recommendations"""
        c.execute(sql)
        for row in c:
            number = row
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))
    return number


def conDetail_add(u_id):

        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()

            sql = """SELECT COUNT(*), user_id FROM connections WHERE user_id = (%d)""" % (int(u_id))
            c.execute(sql)
            for row in c:
                number, user_id = row

            sql = """SELECT COUNT(*),user_id FROM connections_detail WHERE user_id = (%d)""" % (int(u_id))
            c.execute(sql)
            for row in c:
                is_there, user_id = row
            print("isthere")
            print(is_there)

            if is_there == 0:
                sql = """INSERT INTO connections_detail(user_id,num_of_connections)
                                      VALUES (%d, %d )""" % (int(u_id), int(number))
                c.execute(sql)
                conn.commit()
                print(number)
                print("if 0")
            else:
                sql = """UPDATE connections_detail SET num_of_connections = (%d) WHERE user_id = (%d)""" % (int(number), int(u_id))
                c.execute(sql)
                conn.commit()
                print("else")
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))


def conDetail_decrease(u_id):

        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """UPDATE connections_detail SET num_of_connections = num_of_connections - 1 WHERE user_id = (%d)""" % (int(u_id))
            c.execute(sql)
            conn.commit()
            c.close()
            conn.close()
        except Exception as e:
            print(str(e))



def create_recfor_new_user(u_id):

    conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                           passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
    f = '%Y-%m-%d %H:%M:%S'
    c = conn.cursor()

    sql = """SELECT user_type, user_id FROM users WHERE user_id != (%d) AND (SELECT COUNT(*) FROM recommended
                    WHERE recommended.user_id = (%d) AND recommended.following_id=users.user_id) = 0
                    AND (SELECT COUNT(*) FROM connections
                    WHERE connections.user_id = (%d) AND connections.following_id=users.user_id) = 0""" % (int(u_id), int(u_id),int(u_id) )
    c.execute(sql)
    for row in c:
        user_type, user_id = row
        print()
        recommendation_add(u_id, user_id)
    c.close()
    conn.close()
