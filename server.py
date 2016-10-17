import datetime
import os

from flask import Flask
from flask import render_template

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


@app.route('/timeline')
def timeline():
    return render_template('timeline.html')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
