# -*- coding:utf-8 -*-
from webapp import db


class LoginType(db):
    __tablename__ = 'mas_login_type'
    __table_args__ = (
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<LoginType %r>' % self.name


