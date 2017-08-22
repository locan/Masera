# -*- coding:utf-8 -*-
from webapp import db


class LoginType(db.Model):
    __tablename__ = 'mas_login_type'
    __table_args__ = (
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    @classmethod
    def all(cls):
        return cls.query.all()

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<LoginType %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }


