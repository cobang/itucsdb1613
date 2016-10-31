import datetime
import os
import pymysql

from flask import Flask
from flask import render_template, request, redirect, url_for
from connections import Connections,Connection
from posts import Posts, Post
from jobs import Jobs, Job
from users import Users, User
from messages import Message, Chat, Inbox
from random import randint
app = Flask(__name__)
# mysql
MYSQL_DATABASE_HOST = '176.32.230.23'
MYSQL_DATABASE_PORT = 3306
MYSQL_DATABASE_USER = 'cl48-humannet'
MYSQL_DATABASE_PASSWORD = 'itu1773'
MYSQL_DATABASE_DB = 'cl48-humannet'
MYSQL_DATABASE_CHARSET = 'utf8'


@app.route('/test/')
def test_page():
    try:
        c, conn = connection()
        return ("okay")
    except Exception as e:
        return (str(e))


def connection():
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()

        sql = """DROP TABLE IF EXISTS test"""
        c.execute(sql)

        sql = """CREATE TABLE test (
                 FIRST_NAME  CHAR(20) NOT NULL,
                 LAST_NAME  CHAR(20),
                 AGE INT,
                 SEX CHAR(1),
                 INCOME FLOAT )"""

        c.execute(sql)

        sql = """DROP TABLE IF EXISTS posts"""
        c.execute(sql)

        sql = """CREATE TABLE posts(
              POST_ID INT NOT NULL AUTO_INCREMENT,
              USER_ID INT NOT NULL,
              POST_TEXT VARCHAR(100) NOT NULL,
              POST_DATE DATETIME,
              PRIMARY KEY ( POST_ID )
              )"""

        c.execute(sql)

        sql = """DROP TABLE IF EXISTS messages"""
        c.execute(sql)

        sql = """CREATE TABLE messages(
              message_id INT NOT NULL AUTO_INCREMENT,
              content VARCHAR(140),
              message_datetime DATETIME,
              PRIMARY KEY (message_id)
              )"""
        c.execute(sql)

        sql = """DROP TABLE IF EXISTS conversations"""
        c.execute(sql)

        sql = """CREATE TABLE conversations(
              user_id INT NOT NULL,
              participant_id INT NOT NULL,
              in_out INT NOT NULL,
              message_id INT NOT NULL,
              PRIMARY KEY (user_id, message_id)
              )"""
        c.execute(sql)

        sql = """DROP TABLE IF EXISTS connections"""
        c.execute(sql)

        sql = """CREATE TABLE connections(
              user_id INT NOT NULL,
              following_id INT NOT NULL,
              connection_date DATETIME,
              PRIMARY KEY(user_id,following_id)
              )"""
        c.execute(sql)

        sql = """DROP TABLE IF EXISTS jobs"""
        c.execute(sql)

        sql = """CREATE TABLE jobs(
                      JOB_ID INT NOT NULL AUTO_INCREMENT,
                      TITLE VARCHAR(30) NOT NULL,
                      DESCRIPTION VARCHAR(140) NOT NULL,
                      PRIMARY KEY ( JOB_ID )
                      )"""
        c.execute(sql)

        sql = """DROP TABLE IF EXISTS users"""
        c.execute(sql)

        sql = """CREATE TABLE users(
                              id INT NOT NULL AUTO_INCREMENT,
                              name VARCHAR(45) NOT NULL,
                              surname VARCHAR(45) NOT NULL,
                              email VARCHAR(45) NOT NULL,
                              password VARCHAR(45) NOT NULL,
                              PRIMARY KEY ( id )
                              )"""
        c.execute(sql)

        conn.commit()
        c.close()
        conn.close()

        return conn, c
    except Exception as e:
        print(str(e))


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':

        return render_template('home.html')
    else:
        signup()

    return redirect('home')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':

        return render_template('home.html')
    else:
        signup()

    return redirect('home')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_list = Users()
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM users"""

        c.execute(sql)

        for row in c:
            id, name, surname, email, password = row
            user = User(id=id, name=name, surname=surname, email=email, password=password)
            user_list.add_user(user=user)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    users = user_list.get_users()

    if request.method == 'GET':

        return render_template('profile.html', users=users)
    else:
        signup()

    return redirect('profile')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':

        return render_template('about.html')
    else:
        signup()

    return redirect('about')


@app.route('/connections', methods=['GET', 'POST'])
def connections():
    storage = Connections()
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM users"""

        c.execute(sql)
        f = '%Y-%m-%d %H:%M:%S'
        dateTime = datetime.datetime.now()
        for row in c:
            id, name, surname, username, password = row
            connection_new = Connection(120, following_id=id, date=dateTime.strftime(f))
            storage.add_connection(connection=connection_new)
            print("adding")
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    connections_storage = storage.get_connections()

    if request.method == 'GET':
        return render_template('connections.html', connections=connections_storage)
    else:
        signup()
        if 'add_Connection' in request.form:
            dateTime = datetime.datetime.now()
            print("addConnection")
            rec_id = int(request.form['following_id'])
            user_id = randint(0, 1000)
            try:
                conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                                       passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB,
                                       charset=MYSQL_DATABASE_CHARSET)
                c = conn.cursor()
                sql = """INSERT INTO connections(user_id,following_id,connection_date)
                           VALUES (%d, '%d', '%s' )""" % (user_id, rec_id, dateTime.strftime(f))
                c.execute(sql)

                conn.commit()
                c.close()
                conn.close()

            except Exception as e:
                print(str(e))
    return redirect('connections')


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    my_id = 2  # TEMPORARY
    inbox = Inbox()
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """SELECT user_id, participant_id,
                            in_out, content, message_datetime
                  FROM messages, conversations
                  WHERE (messages.message_id = conversations.message_id)
                        AND (user_id = %d)
                  ORDER BY participant_id, datetime""" % my_id
        c.execute(sql)

        old_p = c[0][1]
        chat = Chat()

        for user, participant, in_out, content, msg_datetime in c:
            if in_out == 0:
                sender = user
                receiver = participant
            else:
                sender = participant
                receiver = user

            msg = Message(sender, receiver, content, msg_datetime)

            if old_p == participant:
                chat.add(msg)
            else:
                inbox.add(chat, old_p)
                chat = Chat()
                chat.add(msg)
            old_p = participant

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    if request.method == 'GET':
        chats = inbox.chats
        return render_template('messages.html', chats=chats)
    else:
        if 'send' in request.form:
            participant = request.form['send']
            if int(participant) == 0:
                participant = request.form['username']
            content = request.form['message']
            date = datetime.datetime.now()

            try:
                conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                                       passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB,
                                       charset=MYSQL_DATABASE_CHARSET)
                c = conn.cursor()
                f = '%Y-%m-%d %H:%M:%S'
                sql = """INSERT INTO messages(content, message_datetime)
                          VALUES('%s', '%s')""" % (content, date.strftime(f))
                c.execute(sql)

                sql = """SELECT MAX(message_id) FROM messages"""
                c.execute(sql)
                for x in c:
                    msg_id = x

                sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
                          VALUES(%d, %d ,%d, %d)""" % (my_id, int(participant), 0, msg_id)
                c.execute(sql)
                sql = """INSERT INTO conversations(user_id, participant_id, in_out, message_id)
                          VALUES(%d, %d ,%d, %d)""" % (int(participant), my_id, 1, msg_id)
                c.execute(sql)

                conn.commit()
                c.close()
                conn.close()

            except Exception as e:
                print(str(e))

    return redirect('messages')


@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    store = Posts()
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM posts"""

        c.execute(sql)

        for row in c:
            post_id, user_id, text, date = row
            post = Post(post_id=post_id, user=user_id, text=text, date=date)
            store.add_post(post=post)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    posts = store.get_posts() # "posts" shows exist posts

    if request.method == 'GET':

        return render_template('timeline.html', posts=posts)
    else:
        signup()
        if 'share' in request.form:
            print("share")
            text = request.form['post']
            date = datetime.datetime.now()

            try:
                conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                                       passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
                c = conn.cursor()
                f = '%Y-%m-%d %H:%M:%S'
                sql = """INSERT INTO posts(USER_ID, POST_TEXT, POST_DATE)
                               VALUES (%d, '%s', '%s' )""" % (5, text, date.strftime(f))

                c.execute(sql)

                conn.commit()
                c.close()
                conn.close()

            except Exception as e:
                print(str(e))

        if 'delete' in request.form:
            print("delete")
            print(request.form['delete'])
            post_id = request.form['delete']

            try:
                conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                                       passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB,
                                       charset=MYSQL_DATABASE_CHARSET)
                c = conn.cursor()
                sql = """DELETE FROM posts WHERE POST_ID = (%d) """ % (int(post_id))

                c.execute(sql)

                conn.commit()
                c.close()
                conn.close()

            except Exception as e:
                print(str(e))

    return redirect('timeline')


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    archive = Jobs()
    try:
        conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                               passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB, charset=MYSQL_DATABASE_CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM jobs"""

        c.execute(sql)

        for row in c:
            job_id, title, description = row
            job = Job(job_id=job_id, title=title, description=description)
            archive.add_job(job=job)

        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    jobs_archive = archive.get_jobs()  # "jobs" shows exist jobs

    if request.method == 'GET':

        return render_template('jobs.html', jobs=jobs_archive)
    else:
        signup()
        if 'addJob' in request.form:
            print("addJob")
            title = request.form['title']
            description = request.form['description']

            try:
                conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                                       passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB,
                                       charset=MYSQL_DATABASE_CHARSET)
                c = conn.cursor()
                sql = """INSERT INTO jobs(TITLE, DESCRIPTION)
                                   VALUES ('%s', '%s' )""" % (title, description)

                c.execute(sql)

                conn.commit()
                c.close()
                conn.close()

            except Exception as e:
                print(str(e))

    return redirect('jobs')

def signup():
    if 'signup' in request.form:
        print("Sign Up")
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = pymysql.connect(host=MYSQL_DATABASE_HOST, port=MYSQL_DATABASE_PORT, user=MYSQL_DATABASE_USER,
                                   passwd=MYSQL_DATABASE_PASSWORD, db=MYSQL_DATABASE_DB,
                                   charset=MYSQL_DATABASE_CHARSET)
            c = conn.cursor()
            sql = """INSERT INTO users(name, surname, email, password)
                                   VALUES ('%s', '%s', '%s', '%s' )""" % (name, surname, email, password)

            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()

        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.run(host='0.0.0.0', port=port, debug=debug)
