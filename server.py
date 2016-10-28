import datetime
import os

from flask import Flask
from flask import render_template, request, redirect, url_for

from post import Post
from posts import Posts

app = Flask(__name__)


@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/connections')
def connections():
    return render_template('connections.html')


@app.route('/messages')
def messages():
    return render_template('messages.html')


@app.route('/timeline', methods=['GET', 'POST'])
def timeline():
    if request.method == 'GET':
        posts = app.posts.get_posts()
        #redirect(url_for('site.timeline'))
        return render_template('timeline.html', posts = posts)
    else:
        text = request.form['post']
        date = datetime.datetime.now().ctime()
        user = "ali"
        post = Post(user=user, text=text, date=date)
        app.posts.add_post(post=post)
        posts = app.posts.get_posts()
    return redirect(url_for('timeline', posts=posts))



@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    app.posts = Posts()
    app.run(host='0.0.0.0', port=port, debug=debug)
