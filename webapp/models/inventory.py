# -*- coding:utf-8 -*-
from sqlalchemy.orm.exc import NoResultFound
from webapp import db


class Inventory(db.Model):
    __tablename__ = 'mas_inventory'
    __table_args__ = (

    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    var_file_path = db.Column(db.String(255))
    group_id = db.Column(db.Integer, db.ForeignKey('mas_server_group.id'))
    group = db.relationship('ServerGroup', backref=db.backref('inventorys'))
    memo = db.Column(db.String(255), default='')

    def __init__(self, name=None, group_id=None, memo=None):
        self.name = name
        self.group_id = group_id
        self.memo = memo

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.query.get(_id)
        except NoResultFound:
            return None

    @classmethod
    def get_list(cls, inventory=None, page_no=1, page_size=10):
        try:
            q = []
            query = cls.query
            if inventory:
                if 'name' in inventory:
                    q.append(cls.name == inventory.get('name'))
                if 'group_id' in inventory:
                    q.append(cls.group_id == inventory.get('group_id'))
            data = query.filter(*q).offset((page_no - 1) * page_size).limit(page_size).all()
            data = [s.to_dict() for s in data]
            return {
                'data': data,
                'count': query.filter(*q).count()
            }
        except NoResultFound:
            return None

    def to_dict(self):
        result = {
            'id': self.id,
            'name': self.name,
            'var_file_path': self.var_file_path,
            'group_id': self.group_id,
            'memo': self.memo
        }
        if self.group:
            result['group'] = self.group.name
        return result

    def __repr__(self):
        return '<Inventory %s>' % self.name


class InventoryServer(db.Model):
    __tablename__ = 'mas_inventory_server'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String(50), nullable=False, index=True)
    port = db.Column(db.Integer, default=22)
    ansible_ssh_user = db.Column(db.String)
    ansible_ssh_pass = db.Column(db.String)
    server_id = db.Column(db.Integer, db.ForeignKey('mas_server.id'))
    inventory_group_id = db.Column(db.Integer, db.ForeignKey('mas_inventory_group.id'))
    server = db.relationship('Server', backref=db.backref('inventory_servers'))
    inventory_group = db.relationship('InventoryServerGroup', backref=db.backref('inventory_servers'))

    def __init__(self, host=None, port=None, ansible_ssh_user=None, ansible_ssh_pass=None, server_id=None,
                 inventory_group_id=None):
        self.host = host
        self.port = port
        self.ansible_ssh_user = ansible_ssh_user
        self.ansible_ssh_pass = ansible_ssh_pass
        self.server_id = server_id
        self.inventory_group_id = inventory_group_id

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.query.get(_id)
        except NoResultFound:
            return None

    @classmethod
    def get_list(cls, inventory_server=None, page_no=1, page_size=10):
        try:
            q = []
            query = cls.query
            if inventory_server:
                if 'host' in inventory_server:
                    q.append(cls.host == inventory_server.get('host'))
                if 'inventory_group_id' in inventory_server:
                    q.append(cls.host == inventory_server.get('inventory_group_id'))
            data = query.filter(*q).offset((page_no - 1) * page_size).limit(page_size).all()
            data = [s.to_dict() for s in data]
            return {
                'data': data,
                'count': query.filter(*q).count()
            }

        except NoResultFound:
            return None

    def to_dict(self):
        result = {
            'id': self.id,
            'host': self.host,
            'port': self.port,
            'ansible_ssh_user': self.ansible_ssh_user,
            'ansible_ssh_pass': self.ansible_ssh_pass,
            'server_id': self.server_id,
            'inventory_group_id': self.inventory_group_id
        }
        if self.inventory_group:
            result['inventory_group'] = self.inventory_group.name
        return result

    def __repr__(self):
        return '<InventoryServer %s>' % self.ip


class InventoryServerGroup(db.Model):
    __tablename__ = 'mas_inventory_group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    memo = db.Column(db.String)
    inventory_id = db.Column(db.Integer, db.ForeignKey('mas_inventory.id'))
    inventory = db.relationship('Inventory', backref=db.backref('inventory_server_groups'))
    group_id = db.Column(db.Integer, db.ForeignKey('mas_server_group.id'))
    group = db.relationship('ServerGroup', backref=db.backref('inventory_server_groups'))

    def __init__(self, name, group_id, inventory_id, memo):
        self.name = name
        self.group_id = group_id
        self.memo = memo
        self.inventory_id = inventory_id

    @classmethod
    def get_by_id(cls, _id):
        try:
            return cls.query.get(_id)
        except NoResultFound:
            return None

    @classmethod
    def get_list(cls, inventory_server_group=None, page_no=1, page_size=10):
        try:
            q = []
            query = cls.query
            if inventory_server_group:
                if 'name' in inventory_server_group:
                    q.append(cls.name == inventory_server_group.get('name'))
                if 'group_id' in inventory_server_group:
                    q.append(cls.group_id == inventory_server_group.get('group_id'))
                if 'inventory_id' in inventory_server_group:
                    q.append(cls.inventory_id == inventory_server_group.get('inventory_id'))
            data = query.filter(*q).offset((page_no - 1) * page_size).limit(page_size).all()
            data = [s.to_dict() for s in data]
            return {
                'data': data,
                'count': query.filter(*q).count()
            }
        except NoResultFound:
            return None

    def to_dict(self):
        result = {
            'id': self.id,
            'name': self.name,
            'group_id': self.group_id,
            'inventory_id': self.inventory_id,
            'memo': self.memo
        }
        if self.group:
            result['group'] = self.group.name
        if self.inventory:
            result['inventory'] = self.inventory.name
        return result

    def __repr__(self):
        return '<InventoryServerGroup %s>' % self.name
