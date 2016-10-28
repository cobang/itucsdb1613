from flask import Flask

from handlers import site
from post import Post
from posts import Posts


def create_app():
    app = Flask(__name__)
    app.config.from_object('settings')
    app.register_blueprint(site)

    app.posts = Posts()
    return app


def main():
    app = create_app()
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
