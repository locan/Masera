# -*- utf-8 -*-
from webapp import db


class Server(db.Model):
    __tablename__ = 'mas_server'
    __table_args__ = (
    )

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(30), nullable=False, index=True)
    purpose = db.Column(db.String(255), nullable=False)
    login_type = db.relationship('LoginType', lazy=False)
    position = db.Column(db.String, default='')
    deploy_server = db.Column(db.String, default='')
    memo = db.Column(db.String, default='')

    def __init__(self, ip, purpose, login_type, position, deploy_server, memo):
        self.ip = ip
        self.purpose = purpose
        self.login_type = login_type
        self.position = position
        self.deploy_server = deploy_server
        self.memo = memo

    def __repr__(self):
        return '<Server %r>' % self.ip