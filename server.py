import datetime
import os
import pymysql

from dbconnection import MySQL
from flask import Flask
from flask import render_template, request, redirect, url_for
from connections import Connections,Recommendations, Connection, connection_add, connection_remove, add_to_favorites
from posts import posts_get, post_share, post_delete, post_update
from jobs import job_add, job_edit, job_delete, job_share
from users import user_list, user_edit, user_delete
from messages import get_inbox, send_message, delete_conversation, like_message

app = Flask(__name__)


@app.route('/test/')
def test_page():
    try:
        connection()
        return "okay"
    except Exception as e:
        return str(e)


def connection():
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
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
                      LIKE_NUM INT,
                      DISLIKE_NUM INT,
                      PRIMARY KEY ( POST_ID )
                      )"""

        c.execute(sql)

        sql = """DROP TABLE IF EXISTS messages"""
        c.execute(sql)

        sql = """CREATE TABLE messages(
              message_id INT NOT NULL AUTO_INCREMENT,
              content VARCHAR(140),
              message_datetime DATETIME,
              is_liked INT,
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
              added_to_favorites INT,
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
                              user_id INT NOT NULL AUTO_INCREMENT,
                              user_name VARCHAR(20) NOT NULL,
                              user_surname VARCHAR(20) NOT NULL,
                              user_email VARCHAR(25) NOT NULL,
                              user_password VARCHAR(16) NOT NULL,
                              PRIMARY KEY ( user_id )
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

    users = user_list()

    if request.method == 'GET':

        return render_template('profile.html', users=users)
    else:
        if 'signup' in request.form:
            signup()
        elif 'edit_user' in request.form:
            user_id = request.form['edit_user']
            user_name = request.form['name']
            user_surname = request.form['surname']
            user_edit(user_id, user_name, user_surname)
        elif 'delete_user' in request.form:
            user_id = request.form['delete_user']
            user_delete(user_id=user_id)

    return redirect('profile')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':

        return render_template('about.html')
    else:
        if 'signup' in request.form:
            signup()

    return redirect('about')


@app.route('/connections', methods=['GET', 'POST'])
def connections():
    storage = Recommendations()
    added_Con= Connections()
    try:
        conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                               passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
        c = conn.cursor()
        sql = """SELECT * FROM users"""
        c.execute(sql)
        f = '%Y-%m-%d %H:%M:%S'
        dateTime = datetime.datetime.now()
        for row in c:
            id, name, surname, username, password = row
            connection_new = Connection(120, following_id=id, date=dateTime.strftime(f))
            storage.add_recommendation(connection=connection_new)
            print("adding")
        c.close()
        conn.close()

    except Exception as e:
        print(str(e))

    rec_storage = storage.get_recommendations()
    if request.method == 'GET':
        return render_template('connections.html', recommendations=rec_storage)
    else:
        rec_id = int(request.form['following_id'])
        u_id = int(request.form['user_id'])
        signup()
        if 'add_Connection' in request.form:
            dateTime = datetime.datetime.now()
            print("addConnection")
            key_id = int(request.form['key'])
            storage.delete_recommendation(key=key_id)
            c_new = Connection(120, following_id=rec_id, date=dateTime.strftime(f))
            added_Con.add_connection(c_new)
            print("del")
            connection_add(u_id=u_id,fol_id=rec_id, time=dateTime)
        elif 'remove_Connection' in request.form:
            connection_remove(u_id, rec_id)
        elif 'add_to_favorites' in request.form:
            add_to_favorites(u_id, rec_id)
    return redirect('connections')


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    my_id = 2  # TEMPORARY
    inbox = get_inbox(my_id)

    if request.method == 'GET':
        chats = inbox.chats
        return render_template('messages.html', chats=chats)
    else:
        if 'send' in request.form:
            participant = int(request.form['send'])
            if participant == 0:
                participant = int(request.form['username'])
            content = request.form['message']
            date = datetime.datetime.now()

            send_message(my_id, participant, content, date)

        if 'delete' in request.form:
            participant = int(request.form['delete'])

            delete_conversation(my_id, participant)

        if 'like' in request.form:
            msg_id = int(request.form['like'])

            like_message(msg_id)

    return redirect('messages')


@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    posts = posts_get()

    if request.method == 'GET':
        return render_template('timeline.html', posts=posts)

    else:
        signup()
        if 'share' in request.form:
            print("share")
            text = request.form['post']
            date = datetime.datetime.now()
            user_id = 5
            post_share(user_id=user_id, text=text, date=date)

        if 'delete' in request.form:
            print("delete")
            print(request.form['delete'])
            post_id = request.form['delete']

            post_delete(post_id=post_id)

        if 'like' in request.form:
            print("like")
            print(request.form['like'])
            post_id = request.form['like']
            post_update(post_id, "LIKE_NUM")

        if 'dislike' in request.form:
            print("dislike")
            print(request.form['dislike'])
            post_id = request.form['dislike']
            post_update(post_id, "DISLIKE_NUM")


    return redirect('timeline')


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    jobs_archive = job_share()  # "jobs" shows exist jobs

    if request.method == 'GET':
        return render_template('jobs.html', jobs=jobs_archive)
    else:
        signup()
        if 'addJob' in request.form:
            title = request.form['title']
            description = request.form['description']
            job_add(title, description)

        elif 'editJob' in request.form:
            job_id = request.form['editJob']
            title = request.form['title']
            description = request.form['description']
            job_edit(job_id, title, description)
        elif 'deleteJob' in request.form:
            job_id = request.form['deleteJob']
            job_delete(job_id)

    return redirect('jobs')


def signup():
    if 'signup' in request.form:
        print("Sign Up")
        user_name = request.form['name']
        user_surname = request.form['surname']
        user_email = request.form['email']
        user_password = request.form['password']

        try:
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """INSERT INTO users(user_name, user_surname, user_email, user_password)
                                   VALUES ('%s', '%s', '%s', '%s' )""" % (user_name, user_surname, user_email, user_password)

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
