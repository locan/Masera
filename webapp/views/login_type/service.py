# -*- coding:utf-8 -*-
from webapp.models.login_type import db, LoginType


class LoginTypeService(object):

    @staticmethod
    def save(name):
        login_type = LoginType(name)
        db.session.add(login_type)
        db.session.commit()
        return login_type

    @staticmethod
    def all():
        all = [lt.to_dict() for lt in LoginType.all()]
        return all;

if __name__ == '__main__':
    print LoginTypeService.save('root账号')
