# -*- coding:utf-8 -*-
from webapp import db
from webapp.models import LoginType
from sqlalchemy.exc import IntegrityError


class LoginTypeService(object):

    @staticmethod
    def save(name):
        try:
            login_type = LoginType(name)
            db.session.add(login_type)
            db.session.commit()
            return login_type
        except IntegrityError:
            db.session.rollback()

    @staticmethod
    def alert(_id, name):
        lt = LoginType.query.get(_id)
        lt.name = name
        db.session.commit()

    @staticmethod
    def get_all():
        _all = [lt.to_dict() for lt in LoginType.all()]
        return _all

    @staticmethod
    def get_by_id(_id):
        lt = LoginType.query.get(_id)
        if lt:
            lt = lt.to_dict()
        return lt

    @staticmethod
    def get_list(login_type=None, page_no=1, page_size=10):
        return LoginType.get_list(login_type, page_no, page_size)

    @staticmethod
    def delete_by_ids(ids):
        for _id in ids:
            login_type = LoginType.query.get(_id)
            db.session.delete(login_type)
        db.session.commit()
        return True

if __name__ == '__main__':
    print LoginTypeService.save('root账号')
