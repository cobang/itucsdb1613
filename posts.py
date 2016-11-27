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
    def __init__(self, post_id, user, text, date, like_num=0, likes=Users(), comments=Comments()):
        self.post_id = post_id
        self.user = user
        self.text = text
        self.date = date
        self.like_num = like_num
        self.likes = likes
        self.comments = comments


def posts_get():
    store = Posts()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM posts"""

        c.execute(sql)

        for row in c:
            post_id, user_id, text, date, like_num = row
            post = Post(post_id=post_id, user=user_id, text=text, date=date, like_num=like_num,
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
        sql = """INSERT INTO posts(USER_ID, POST_TEXT, POST_DATE, LIKE_NUM)
                       VALUES (%d, '%s', '%s', %d)""" % (user_id, text, date.strftime(f), 0)

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
        sql = """DELETE FROM posts WHERE POST_ID = (%d) """ % (int(post_id))
        print(sql)
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def post_update(post_id, action):
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()

        user_id = 7 # degisecek
        if action == "LIKE_NUM":
            sql = """UPDATE posts SET LIKE_NUM = LIKE_NUM +1  WHERE POST_ID = %d """ % (int(post_id))
            c.execute(sql)
            sql = """INSERT INTO likes ( user_id, posts_post_id )
                       VALUES( %d, %d )""" % (user_id, int(post_id))
            c.execute(sql)
        elif action == "DISLIKE_NUM":
            sql = """UPDATE posts SET LIKE_NUM = LIKE_NUM -1  WHERE POST_ID = %d """ % (int(post_id))
            c.execute(sql)
            sql = """DELETE FROM likes WHERE %d = user_id and %d = posts_post_id""" % (user_id,int(post_id))
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

        print(sql)
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
        sql = """SELECT users.user_id, user_name, user_surname FROM users INNER JOIN
                (SELECT user_id FROM likes WHERE %d=posts_post_id) AS who_like
                ON users.user_id IN (who_like.user_id)""" % post_id

        c.execute(sql)
        for row in c:
            user_id, user_name, user_surname = row
            user = User(user_id=user_id, user_name=user_name, user_surname=user_surname)
            store.add_user(user=user)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    return store.get_users()


def get_post_comments(id_post):
    store = Comments()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT comment_id, comment_text, comment_date,
post_id, users.user_id, user_name, user_surname
 FROM users INNER JOIN
(SELECT * FROM comment WHERE %d = post_id) AS comments
ON users.user_id = comments.user_id
""" % id_post

        c.execute(sql)
        for row in c:
            comment_id, comment_text, comment_date, post_id, user_id, user_name, user_surname = row
            comment = Comment(comment_id=comment_id, comment_text=comment_text, comment_date=comment_date,
                              post_id=post_id, user_id=user_id, user_name=user_name, user_surname=user_surname)

            store.add_comment(comment)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    return store.get_comments()
