# -*- coding:utf-8 -*-
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from webapp import db


class User(UserMixin, db.Model):
    __tablename__ = 'mas_user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column('password', db.String(255))

    def __init__(self):
        pass

    def get_by_username(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return None

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username
