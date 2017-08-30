# -*- coding: utf-8 -*-
from webapp import db
from webapp.models import ServerGroup
from sqlalchemy.exc import IntegrityError


class ServerGroupService(object):
    @staticmethod
    def add(name, memo):
        try:
            group = ServerGroup(name, memo)
            db.session.add(group)
            db.session.commit()
            return group
        except IntegrityError:
            db.session.rollback()
            return None

    @staticmethod
    def alert(_id, name, memo):
        try:
            sg = ServerGroup.query.get(_id)
            sg.name = name
            sg.memo = memo
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @staticmethod
    def get_all():
        groups = ServerGroup.all()
        groups = [g.to_dict() for g in groups]
        return groups

    @staticmethod
    def get_by_id(id):
        g = ServerGroup.query.get(id)
        if g:
            g = g.to_dict()
        return g

    @staticmethod
    def get_list(group=None, page_no=1, page_size=10):
        return ServerGroup.get_list(group, page_no, page_size)

    @staticmethod
    def delete_by_ids(ids):
        for _id in ids:
            group = ServerGroup.query.get(_id)
            db.session.delete(group)
        db.session.commit()
        return True
