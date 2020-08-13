from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from .config import Config
from .models import UserModel

from .auth import auth
from .application import application 

login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(username):
    return UserModel.query(username)


def create_app():
    # init
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    login_manager.init_app(app)

    # config
    app.config.from_object(Config)

    # blueprints
    app.register_blueprint(auth)
    app.register_blueprint(application)

    return app
