# -*- coding:utf-8 -*-
from webapp import db


class ServerGroup(db):
    __tablename__ = 'mas_server_group'
    __table_args__ = (
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    memo = db.Column(db.String, default='')

    def __init__(self, name, memo):
        self.name = name
        self.memo = memo

    def __repr__(self):
        return '<Group %r>' % self.name

