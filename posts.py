import pymysql


class Posts:
    def __init__(self):
        self.posts = {}
        self.key = 0

    def add_post(self, post):
        self.key += 1
        post.key = self.key
        self.posts[self.key] = post

    def delete_post(self, key):
        del self.posts[key]

    def get_post(self, key):
        return self.posts[key]

    def get_posts(self):
        return sorted(self.posts.items())


class Post:
    def __init__(self, post_id, user, text, date, like_num=0, dislike_num=0):
        self.post_id = post_id
        self.user = user
        self.text = text
        self.date = date
        self.like_num = like_num
        self.dislike_num = dislike_num

# mysql
MYSQL_DATABASE_HOST = '176.32.230.23'
MYSQL_DATABASE_PORT = 3306
MYSQL_DATABASE_USER = 'cl48-humannet'
MYSQL_DATABASE_PASSWORD = 'itu1773'
MYSQL_DATABASE_DB = 'cl48-humannet'
MYSQL_DATABASE_CHARSET = 'utf8'


def posts_get():
    store = Posts()
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM posts"""

        c.execute(sql)

        for row in c:
            post_id, user_id, text, date, like_num, dislike_num = row
            post = Post(post_id=post_id, user=user_id, text=text, date=date, like_num=like_num, dislike_num=dislike_num)
            store.add_post(post=post)

        c.close()
        conn.close()
        return store.get_posts()

    except Exception as e:
        print(str(e))
        return store.get_posts()


def post_share(user_id, text, date):
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        f = '%Y-%m-%d %H:%M:%S'
        sql = """INSERT INTO posts(USER_ID, POST_TEXT, POST_DATE, LIKE_NUM, DISLIKE_NUM)
                       VALUES (%d, '%s', '%s', %d, %d )""" % (user_id, text, date.strftime(f), 0, 0)

        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def post_delete(post_id):
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB,
                               charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """DELETE FROM posts WHERE POST_ID = (%d) """ % (int(post_id))
        print(sql)
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))


def post_update(post_id, tuple_name):
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB,
                               charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """UPDATE posts SET %s = %s +1  WHERE POST_ID = %d """ % (tuple_name, tuple_name, int(post_id))

        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))