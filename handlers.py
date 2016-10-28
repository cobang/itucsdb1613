from flask import Blueprint, render_template
from flask import current_app
from flask import request
from flask import redirect, url_for

from datetime import datetime

from post import Post
site = Blueprint('site', __name__)


@site.route('/')
def home_page():
    now = datetime.now()
    return render_template('home.html', current_time=now.ctime())


@site.route('/home')
def home():
    return render_template('home.html')


@site.route('/profile')
def profile():
    return render_template('profile.html')


@site.route('/about')
def about():
    return render_template('about.html')


@site.route('/connections')
def connections():
    return render_template('connections.html')


@site.route('/messages')
def messages():
    return render_template('messages.html')


@site.route('/timeline', methods=['GET', 'POST'])
def timeline():
    if request.method == 'GET':
        posts = current_app.posts.get_posts()
        #redirect(url_for('site.timeline'))
        return render_template('timeline.html', posts = posts)
    else:
        text = request.form['post']
        date = datetime.now()
        user = "ali"
        post = Post(user=user, text=text, date=date)
        current_app.posts.add_post(post=post)
        posts = current_app.posts.get_posts()
    return redirect(url_for('site.timeline', posts = posts))


@site.route('/jobs')
def jobs():
    return render_template('jobs.html')

