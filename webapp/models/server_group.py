# -*- coding:utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound

from webapp import db


class ServerGroup(db.Model):
    __tablename__ = 'mas_server_group'
    __table_args__ = (
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    memo = db.Column(db.String, default='')

    def __init__(self, name, memo):
        self.name = name
        self.memo = memo

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_list(cls, group=None, page_no=1, page_size=10):
        try:
            q = []
            query = cls.query
            if group:
                if 'name' in group:
                    q.append(cls.name == group.get('name'))
            data = query.filter(*q).offset((page_no - 1) * page_size).limit(page_size).all()
            data = [g.to_dict() for g in data]
            return {
                'data': data,
                'count': query.filter(*q).count()
            }
        except NoResultFound:
            return None

    def __repr__(self):
        return '<Group %r>' % self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'memo': self.memo
        }


if __name__ == '__main__':
    print ServerGroup.all()
