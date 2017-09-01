# -*- coding:utf-8 -*-


from flask import Flask, request
from flask_login import LoginManager
from flask_login.utils import current_user, current_app
from flask_sqlalchemy import SQLAlchemy

from webapp.common.functional import get_reg_blueprint

app = Flask(__name__, instance_relative_config=True, static_url_path='')
app.config.from_object('webapp.settings')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'webapp.views.login.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from webapp.models import User
    return User.query.get(user_id)


for bl in get_reg_blueprint(app.config.get('APP_PATH'), ['users', ]):
    app.register_blueprint(blueprint=bl)

# 这里配置url中需要登录验证的关键字
LOGIN_REQUIRED_FILTER = set(['server', 'inventory'])


def user_valid():
    url = str(request.url)
    #print url
    url_split = url.split('/')
    print url_split
    if LOGIN_REQUIRED_FILTER & set(url_split):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()


app.before_request(user_valid)
