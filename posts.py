import pymysql
from dbconnection import MySQL
from users import Users, User


class Comments:
    def __init__(self,):
        self.comments = {}
        self.key = 0

    def add_comment(self, comment):
        self.key += 1
        self.comments[self.key] = comment

    def delete_comment(self, key):
        del self.comments[key]

    def get_comment(self, key):
        return self.comments[key]

    def get_comments(self):
        return sorted(self.comments.items())


class Comment:
    def __init__(self, comment_id, comment_text, comment_date, post_id, user_id, user_name=" ", user_surname=" "):
        self.comment_id = comment_id
        self.comment_text = comment_text
        self.comment_date = comment_date
        self.post_id = post_id
        self.user_id = user_id
        self.user_name = user_name
        self.user_surname = user_surname


class Posts:
    def __init__(self):
        self.posts = {}
        self.key = 0

    def add_post(self, post):
        self.key += 1
        self.posts[self.key] = post

    def delete_post(self, key):
        del self.posts[key]

    def get_post(self, key):
        return self.posts[key]

    def get_posts(self):
        return sorted(self.posts.items())


class Post:
    def __init__(self, post_id, user, text, date, user_name=" ", like_num=0, likes=Users(), comments=Comments()):
        self.post_id = post_id
        self.user = user
        self.text = text
        self.date = date
        self.user_name = user_name
        self.like_num = like_num
        self.likes = likes
        self.comments = comments


def posts_get(current_user_id):
    store = Posts()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """SELECT P1.post_id, P1.user_id, post_text,post_date,like_num, name FROM
(SELECT T1.post_id, user_id, post_text,post_date,like_num FROM (SELECT *  FROM posts INNER JOIN
(SELECT following_id FROM connections where user_id = %d
UNION SELECT user_id FROM connections where user_id= %d) AS follow
ON posts.user_id = follow.following_id) AS T1 LEFT JOIN
(SELECT post_id, COUNT(*) AS like_num FROM likes GROUP BY post_id) AS T2
ON T1.post_id = T2.post_id) AS P1 LEFT JOIN (SELECT u.user_id ,(CASE
                          WHEN u.user_type = 3
                              THEN uni.university_name
                          WHEN u.user_type = 2
                              THEN com.company_name
                          WHEN u.user_type = 1
                              THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                          ELSE
                              NULL
                        END)AS name
                  FROM users AS u
                  LEFT JOIN user_detail AS ud
                      ON ud.user_id = u.user_id
                  LEFT JOIN university_detail AS uni
                      ON uni.user_id = u.user_id
                  LEFT JOIN company_detail AS com
                      ON com.user_id = u.user_id
                  ) AS P2 ON P1.user_id= P2.user_id;""" % (current_user_id, current_user_id)
        c.execute(sql)

        for row in c:
            post_id, user_id, post_text, post_date, like_num, name = row

            if like_num == None:
                like_num = 0

            post = Post(post_id=post_id, user=user_id, text=post_text, date=post_date,
                        like_num=like_num, user_name=name,
                        likes=get_likes(post_id), comments=get_post_comments(post_id))
            store.add_post(post=post)

        c.close()
        conn.close()
        return store.get_posts()

    except Exception as e:
        print(str(e))
        return store.get_posts()


def post_share(user_id, text, date):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        sql = """INSERT INTO posts(USER_ID, POST_TEXT, POST_DATE)
                       VALUES (%d, '%s', '%s')""" % (user_id, text, date.strftime(f))
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def post_delete(post_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """DELETE FROM comment WHERE post_id = (%d) """ % (int(post_id))
        c.execute(sql)

        sql = """DELETE FROM likes WHERE post_id = (%d) """ % (int(post_id))
        c.execute(sql)

        sql = """DELETE FROM posts WHERE POST_ID = (%d) """ % (int(post_id))
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def post_update(post_id, action, current_user_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        if action == "LIKE_NUM":
            sql = """INSERT INTO likes ( user_id, post_id )
                       VALUES( %d, %d )""" % (current_user_id, int(post_id))
            c.execute(sql)
        elif action == "DISLIKE_NUM":
            sql = """DELETE FROM likes WHERE %d = user_id and %d = post_id""" % (current_user_id, int(post_id))
            c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def update_post_text(text, post_id, date):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        f = '%Y-%m-%d %H:%M:%S'
        sql = """UPDATE posts SET post_text = '%s', post_date = '%s'  WHERE post_id = %d """ % (text, date.strftime(f), int(post_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def update_comment_text(text, comment_id, date):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        f = '%Y-%m-%d %H:%M:%S'
        sql = """UPDATE comment SET comment_text = '%s', comment_date = '%s'  WHERE comment_id = %d """ % (text, date.strftime(f), int(comment_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def delete_comment(comment_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """DELETE FROM comment WHERE comment_id = (%d) """ % (int(comment_id))
        c.execute(sql)
        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def post_comment_add(comment_text, post_id, date, user_id):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        f = '%Y-%m-%d %H:%M:%S'
        sql = """INSERT INTO comment(comment_text, comment_date, post_id, user_id)
                               VALUES ('%s', '%s', '%s', %d)""" % (comment_text, date.strftime(f), int(post_id), user_id)

        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def get_likes(post_id):
    store = Users()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT P1.user_id,  P1.user_type, name  FROM
(SELECT users.user_id, user_type FROM users INNER JOIN
                (SELECT user_id FROM likes WHERE post_id= %d) AS who_like
                ON users.user_id IN (who_like.user_id)) AS P1 LEFT JOIN (SELECT u.user_id ,(CASE
                          WHEN u.user_type = 3
                              THEN uni.university_name
                          WHEN u.user_type = 2
                              THEN com.company_name
                          WHEN u.user_type = 1
                              THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                          ELSE
                              NULL
                        END)AS name
                  FROM users AS u
                  LEFT JOIN user_detail AS ud
                      ON ud.user_id = u.user_id
                  LEFT JOIN university_detail AS uni
                      ON uni.user_id = u.user_id
                  LEFT JOIN company_detail AS com
                      ON com.user_id = u.user_id
                  ) AS P2 ON P1.user_id= P2.user_id""" % post_id

        c.execute(sql)

        for row in c:
            user_id, user_type, user_name = row
            user = User(user_id=user_id, user_type=user_type, user_name=user_name)
            store.add_user(user=user)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    return store.get_users()


def posts_get_name(user_id):
    try:
        user_name = "NAME"
        user_surname = "SURNAME"
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """SELECT user_type FROM users WHERE user_id = %d""" % user_id
        c.execute(sql)
        for row in c:
            user_type = row[0]

        if user_type==1 :
            sql = """SELECT user_name, user_surname FROM user_detail WHERE user_id = %d""" % user_id
            c.execute(sql)

            for row in c:
                user_name, user_surname = row
                user_name = user_name + " " + user_surname

        elif user_type == 2:
            sql = """SELECT company_name FROM company_detail WHERE user_id = %d""" % user_id
            c.execute(sql)
            for row in c:
                company_name = row[0]
                user_name = company_name

        elif user_type == 3:
            sql = """SELECT university_name FROM university_detail WHERE user_id = %d""" % user_id
            c.execute(sql)
            for row in c:
                university_name = row[0]
                user_name = university_name

        c.close()
        conn.close()
    except Exception as e:
        print(str(e))

    return user_name


def get_post_comments(id_post):
    store = Comments()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT P1.*, name FROM
(SELECT comment_id, comment_text, comment_date,
post_id, users.user_id
 FROM users INNER JOIN
(SELECT * FROM comment WHERE post_id = %d) AS comments
ON users.user_id = comments.user_id) AS P1 LEFT JOIN (SELECT u.user_id ,(CASE
                          WHEN u.user_type = 3
                              THEN uni.university_name
                          WHEN u.user_type = 2
                              THEN com.company_name
                          WHEN u.user_type = 1
                              THEN CONCAT_WS(' ', ud.user_name, ud.user_surname)
                          ELSE
                              NULL
                        END)AS name
                  FROM users AS u
                  LEFT JOIN user_detail AS ud
                      ON ud.user_id = u.user_id
                  LEFT JOIN university_detail AS uni
                      ON uni.user_id = u.user_id
                  LEFT JOIN company_detail AS com
                      ON com.user_id = u.user_id
                  ) AS P2 ON P1.user_id= P2.user_id
""" % id_post

        c.execute(sql)
        for row in c:
            comment_id, comment_text, comment_date, post_id, user_id, user_name = row
            comment = Comment(comment_id=comment_id, comment_text=comment_text, comment_date=comment_date,
                              post_id=post_id, user_id=user_id, user_name= user_name)

            store.add_comment(comment)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    return store.get_comments()


def get_like_num(post_id):
    try:
        like_num = 0
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        sql = """SELECT COUNT(user_id) AS like_num FROM likes WHERE post_id = %d""" % post_id
        c.execute(sql)

        for row in c:
            like_num = row[0]

        c.close()
        conn.close()
        return like_num
    except Exception as e:
        print(str(e))
        return like_num