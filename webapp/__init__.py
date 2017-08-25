# -*- coding:utf-8 -*-


from flask import Flask, request
from flask_login import LoginManager
from flask_login.utils import current_user, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect

from webapp import views
from webapp.common.functional import get_reg_blueprint

app = Flask(__name__, instance_relative_config=True, static_url_path='')
app.config.from_object('webapp.settings')
db = SQLAlchemy(app)

# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'webapp.views.login.login'
login_manager.init_app(app)

from webapp.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


for bl in get_reg_blueprint(app.config.get('APP_PATH'), ['users', ]):
    app.register_blueprint(blueprint=bl)


def user_valid():
    if 'webapp.views.login.login' == request.endpoint:
        pass
    elif not current_user.is_authenticated:
        return current_app.login_manager.unauthorized()


app.before_request(user_valid)
