# -*- coding:utf-8 -*-

from webapp import db
from webapp.models.server import Server
from webapp.models.login_type import LoginType


class ServerService(object):
    @staticmethod
    def add(ip, purpose, login_type, position, deploy_server, memo):
        server = Server(ip, purpose, position, deploy_server, memo)
        l = LoginType.query.filter(LoginType.name == login_type).first()
        if not l:
            l = LoginType(name=login_type)
            db.session.add(l)

        server._login_type = l
        db.session.add(server)
        db.session.commit()
        return server

    @staticmethod
    def alert(server):
        pass

    @staticmethod
    def delete(id):
        server = Server.get_by_id(id)
        db.session.delete(server)
        db.session.commit()
        return server

    @staticmethod
    def get_list(server=None, page_no=1, page_size=10):
        return Server.get_list(server, page_no, page_size)

    @staticmethod
    def get_by_id(id):
        return Server.get(id)


if __name__ == '__main__':
    # ServerService.add('10.108.76.75/220.181.159.75', u'开发服务器', '1', None, None, '13123')
    s = Server(position='1')

    a = ServerService.get_list(page_no=1, page_size=2)
    for i in a:
        print i
