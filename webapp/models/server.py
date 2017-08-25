# -*- utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from webapp import db


class Server(db.Model):
    __tablename__ = 'mas_server'
    __table_args__ = (
    )

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(30), nullable=False, index=True)
    purpose = db.Column(db.String(255), nullable=False)
    position = db.Column(db.String, default='')
    deploy_server = db.Column(db.String, default='')
    memo = db.Column(db.String, default='')
    login_type_id = db.Column('login_type', db.Integer, db.ForeignKey('mas_login_type.id'))
    group_id = db.Column(db.Integer, db.ForeignKey('mas_server_group.id'))

    login_type = db.relationship('LoginType', backref=db.backref('server'))
    group = db.relationship('ServerGroup', backref=db.backref('servers'))

    def __init__(self, ip=None, purpose=None, position=None, deploy_server=None, memo=None):
        self.ip = ip
        self.purpose = purpose
        self.position = position
        self.deploy_server = deploy_server
        self.memo = memo

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.query.filter_by(id=id).one()
        except NoResultFound:
            return None

    @classmethod
    def get_list(cls, server=None, page_no=1, page_size=10):
        try:
            q = []
            query = cls.query
            if server:
                if 'ip' in server:
                    q.append(cls.ip == server.get('ip'))
                if 'group' in server:
                    q.append(cls.group_id == server.get('group'))
                if 'position' in server:
                    q.append(cls.position == server.get('position'))
                if 'deploy_server' in server:
                    q.append(cls.deploy_server == server.get('deploy_server'))
                if 'login_type' in server:
                    q.append(cls.login_type == server.get('login_type'))
                if 'purpose' in server:
                    q.append(cls.purpose == server.get('purpose'))
            data = query.filter(*q).offset((page_no - 1) * page_size).limit(page_size).all()
            data = [s.to_dict() for s in data]
            return {
                'data': data,
                'count': query.filter(*q).count()
            }
        except NoResultFound:
            return None

    def __repr__(self):
        return '<Server %r>' % self.ip

    def to_dict(self):
        result = {
            'id': self.id,
            'ip': self.ip,
            'purpose': self.purpose,
            'position': self.position,
            'deploy_server': self.deploy_server,
            'login_type_id': self.login_type_id,
            'group_id': self.group_id,
            'memo': self.memo
        }
        if self.group:
            result['group'] = self.group.name
        if self.login_type:
            result['login_type'] = self.login_type.name
        return result
