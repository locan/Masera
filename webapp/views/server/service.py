# -*- coding:utf-8 -*-

from webapp import db
from webapp.models import Server


class ServerService(object):
    @staticmethod
    def add(ip, group, purpose, login_type, position, deploy_server, memo):
        server = Server(ip, purpose, position, deploy_server, memo)
        server.login_type_id = login_type
        server.group_id = group
        db.session.add(server)
        db.session.commit()
        return server

    @staticmethod
    def alert(_id, ip, group, purpose, login_type, position, deploy_server, memo):
        server = Server.query.get(_id)
        server.ip = ip
        server.purpose = purpose
        server.position = position
        server.deploy_server = deploy_server
        server.memo = memo
        server.login_type_id = login_type
        server.group_id = group
        server.id = _id
        db.session.commit()
        return server

    @staticmethod
    def delete(id):
        server = Server.get_by_id(id)
        db.session.delete(server)
        db.session.commit()
        return server

    @staticmethod
    def delete_by_ids(ids):
        for id in ids:
            server = Server.get_by_id(id)
            db.session.delete(server)
        db.session.commit()
        return True

    @staticmethod
    def get_list(server=None, page_no=1, page_size=10):
        return Server.get_list(server, page_no, page_size)

    @staticmethod
    def get_by_id(id):
        s = Server.get_by_id(id)
        if s:
            s = s.to_dict()
        return s


if __name__ == '__main__':
    # ServerService.add('10.108.76.75/220.181.159.75', u'开发服务器', '1', None, None, '13123')
    s = Server(position='1')

    a = ServerService.get_list(page_no=1, page_size=2)
    for i in a:
        print i
