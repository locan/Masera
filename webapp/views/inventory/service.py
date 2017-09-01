# -*- coding:utf-8 -*-

from webapp import db
from webapp.models import Inventory, InventoryServer, InventoryServerGroup
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
            db.session.rollback()
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


class InventoryGroupService(object):
    @staticmethod
    def add(name, group_id, inventory_id, memo):
        try:
            _isg = InventoryServerGroup(name=name,
                                        group_id=group_id,
                                        inventory_id=inventory_id,
                                        memo=memo)
            db.session.add(_isg)
            db.session.commit()
            return _isg
        except IntegrityError:
            db.session.rollback()
            return None

    @staticmethod
    def alter(_id, name, group_id, inventory_id, memo):
        try:
            _isg = InventoryServerGroup.get_by_id(_id)
            _isg.name = name
            _isg.group_id = group_id
            _isg.inventory_id = inventory_id
            _isg.memo = memo
            db.session.commit()
            return _isg
        except IntegrityError:
            return None

    @staticmethod
    def delete_by_ids(ids):
        for _id in ids:
            isg = InventoryServerGroup.get_by_id(_id)
            db.session.delete(isg)
        db.session.commit()

    @staticmethod
    def get_list(_group, page_no=1, page_size=10):
        return InventoryServerGroup.get_list(_group, page_no, page_size)


class InventoryServerService(object):
    @staticmethod
    def add(host=None, port=None, ansible_ssh_user=None, ansible_ssh_pass=None, server_id=None,
            inventory_group_id=None):
        try:
            inventory = InventoryServer(host=host,
                                        port=port,
                                        ansible_ssh_user=ansible_ssh_user,
                                        ansible_ssh_pass=ansible_ssh_pass,
                                        server_id=server_id,
                                        inventory_group_id=inventory_group_id)
            db.session.add(inventory)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @staticmethod
    def alert(_id=None, host=None, port=None, ansible_ssh_user=None, ansible_ssh_pass=None, server_id=None,
            inventory_group_id=None):
        pass