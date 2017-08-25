# -*- coding:utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound

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

    @classmethod
    def get_list(cls, login_type=None, page_no=1, page_size=10):
        try:
            q = []
            query = cls.query
            if login_type:
                if 'name' in login_type:
                    q.append(cls.name == login_type.get('name'))
            data = query.filter(*q).offset((page_no - 1) * page_size).limit(page_size).all()
            data = [lt.to_dict() for lt in data]
            return {
                'data': data,
                'count': query.filter(*q).count()
            }
        except NoResultFound:
            return None

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<LoginType %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
