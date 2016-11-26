import datetime
import os
import pymysql

from dbconnection import MySQL
from flask import Flask
from flask import render_template, request, redirect, url_for
from connections import Connections, Recommendations, Connection, connection_add, connection_remove, add_to_favorites
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

        sql = """
-- -----------------------------------------------------
-- Table `cl48-humannet`.`university`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `university` (
  `university_id` INT NOT NULL,
  `university_email` VARCHAR(45) NOT NULL,
  `university_password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`university_id`))
DEFAULT CHARACTER SET = utf8;
        """
        c.execute(sql)

        sql = """
-- -----------------------------------------------------
-- Table `cl48-humannet`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `company_id` INT NULL,
  `university_id` INT NULL,
  `user_name` VARCHAR(20) NOT NULL,
  `user_surname` VARCHAR(20) NOT NULL,
  `user_email` VARCHAR(25) NOT NULL,
  `user_password` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`user_id`),
  INDEX `fk_users_company1_idx` (`company_id` ASC),
  INDEX `fk_users_university1_idx` (`university_id` ASC),
  CONSTRAINT `fk_users_company1`
    FOREIGN KEY (`company_id`)
    REFERENCES `cl48-humannet`.`company` (`company_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_university1`
    FOREIGN KEY (`university_id`)
    REFERENCES `cl48-humannet`.`university` (`university_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
DEFAULT CHARACTER SET = utf8;
        """

        c.execute(sql)

        sql = """
-- -----------------------------------------------------
-- Table `cl48-humannet`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `location` (
  `location_id` INT NOT NULL,
  `location_state` VARCHAR(45) NOT NULL,
  `location_country` VARCHAR(45) NOT NULL,
  `location_zipcode` VARCHAR(45) NULL,
  PRIMARY KEY (`location_id`))
DEFAULT CHARACTER SET = utf8;
        """

        c.execute(sql)

        sql = """
-- -----------------------------------------------------
-- Table `cl48-humannet`.`user_detail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cl48-humannet`.`user_detail` (
  `user_id` INT NOT NULL,
  `date_of_birth` DATE NULL,
  `phone` VARCHAR(15) NULL,
  `address` VARCHAR(45) NULL,
  `location_location_id` INT NOT NULL,
  INDEX `fk_user_detail_users1_idx` (`user_id` ASC),
  INDEX `fk_user_detail_location1_idx` (`location_location_id` ASC),
  PRIMARY KEY (`user_id`),
  CONSTRAINT `fk_user_detail_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `cl48-humannet`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_detail_location1`
    FOREIGN KEY (`location_location_id`)
    REFERENCES `cl48-humannet`.`location` (`location_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
DEFAULT CHARACTER SET = utf8;
        """

        c.execute(sql)

        sql = """
-- -----------------------------------------------------
-- Table `cl48-humannet`.`university_detail`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `university_detail` (
  `university_id` INT NOT NULL,
  `university_name` VARCHAR(45) NULL,
  `university_address` VARCHAR(45) NULL,
  `location_id` INT NOT NULL,
  INDEX `fk_university_detail_university1_idx` (`university_id` ASC),
  INDEX `fk_university_detail_location1_idx` (`location_id` ASC),
  PRIMARY KEY (`university_id`),
  CONSTRAINT `fk_university_detail_university1`
    FOREIGN KEY (`university_id`)
    REFERENCES `cl48-humannet`.`university` (`university_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_university_detail_location1`
    FOREIGN KEY (`location_id`)
    REFERENCES `cl48-humannet`.`location` (`location_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
DEFAULT CHARACTER SET = utf8;
        """

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
            storage.delet_byid(user_id)
    return redirect('profile')


@app.route('/about', methods=['GET', 'POST'])
def about():
    if request.method == 'GET':

        return render_template('about.html')
    else:
        if 'signup' in request.form:
            signup()

    return redirect('about')


storage = Recommendations()
added_Con = Connections()


@app.route('/connections', methods=['GET', 'POST'])
def connections():
    try:
        if storage.get == 0 or storage.key == 0:
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
            storage.get = 1
        elif storage.get == 2:
            print("pof adding")
            conn = pymysql.connect(host=MySQL.HOST, port=MySQL.PORT, user=MySQL.USER,
                                   passwd=MySQL.PASSWORD, db=MySQL.DB, charset=MySQL.CHARSET)
            c = conn.cursor()
            sql = """SELECT * FROM users"""
            c.execute(sql)
            f = '%Y-%m-%d %H:%M:%S'
            dateTime = datetime.datetime.now()
            for row in c:
                id, name, surname, username, password = row
                if storage.is_item(id=id) == 1:
                    connection_new = Connection(120, following_id=id, date=dateTime.strftime(f))
                    storage.add_recommendation(connection=connection_new)
                    print("new adding")
            storage.get = 1
        else:
            print("added once")
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
        key_id = int(request.form['key'])
        if 'add_Connection' in request.form:
            dateTime = datetime.datetime.now()
            print("addConnection")
            storage.delete_recommendation(key=key_id)
            f = '%Y-%m-%d %H:%M:%S'
            c_new = Connection(120, following_id=rec_id, date=dateTime.strftime(f))
            added_Con.add_connection(c_new)
            print("del")
            connection_add(u_id=u_id, fol_id=rec_id, time=dateTime)
        elif 'add_to_favorites' in request.form:
            add_to_favorites(u_id, rec_id)
    return redirect('connections')


@app.route('/added_connections', methods=['GET', 'POST'])
def added_connections():
    added = added_Con.get_connections()
    if request.method == 'GET':
        return render_template('added_connections.html', connections=added)
    else:
        rec_id = int(request.form['following_id'])
        u_id = int(request.form['user_id'])
        signup()
        f = '%Y-%m-%d %H:%M:%S'
        dateTime = datetime.datetime.now()
        if 'remove_Connection' in request.form:
            connection_remove(u_id, rec_id)
            c_new = Connection(120, following_id=rec_id, date=dateTime.strftime(f))
            storage.add_recommendation(c_new)
            key_id = int(request.form['key'])
            added_Con.delete_connection(counter=key_id)
        elif 'add_to_favorites' in request.form:
            add_to_favorites(u_id, rec_id)

    return redirect('added_connections')


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
                                   VALUES ('%s', '%s', '%s', '%s' )""" % (
            user_name, user_surname, user_email, user_password)

            c.execute(sql)

            conn.commit()
            c.close()
            conn.close()
            storage.get = 2

        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.run(host='0.0.0.0', port=port, debug=debug)
