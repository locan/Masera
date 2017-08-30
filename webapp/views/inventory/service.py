# -*- coding:utf-8 -*-

from webapp import db
from webapp.models import Inventory
from sqlalchemy.exc import IntegrityError


class InventoryService(object):
    @staticmethod
    def add(name, group_id, memo):
        try:
            inventory = Inventory(name, group_id, memo)
            db.session.add(inventory)
            db.session.commit()
            return inventory
        except IntegrityError:
            db.session.rollback()
            return None

    @staticmethod
    def alert(_id, name, group_id, memo):
        try:
            inventory = Inventory.query.get(_id)
            inventory.name = name
            inventory.group_id = group_id
            inventory.memo = memo
            db.session.commit()
            return inventory
        except IntegrityError:
            return None

    @staticmethod
    def delete_by_ids(ids):
        for _id in ids:
            inventory = Inventory.get_by_id(_id)
            db.session.delete(inventory)
        db.session.commit()
        return True

    @staticmethod
    def get_list(inventory, page_no=1, page_size=10):
        return Inventory.get_list(inventory=inventory, page_no=page_no, page_size=page_size)

    @staticmethod
    def get_by_id(_id):
        return Inventory.get_by_id(_id)
