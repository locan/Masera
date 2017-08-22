# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, request, jsonify, make_response

from service import ServerService
from webapp.views.server import blueprint
from webapp.views.login_type.service import LoginTypeService


@blueprint.route('/server/index', methods=['GET'])
def index():
    return render_template('server/list.html')


@blueprint.route('/server/list', methods=['GET', 'POST'])
def get_page_list():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('limit', 20))
    server = request.args.get('server', None)
    server_list = ServerService.get_list(server, page, size)
    # return render_template('server/list.html', servers=server_list)
    server_list.update({'code': 0})
    return jsonify(server_list)


@blueprint.route('/server/add', methods=['GET'])
def add():
    ft = '编辑'
    lts = LoginTypeService.all()
    return render_template('server/form.html', form_type=ft, login_type_list=lts)


@blueprint.route('/server/form/add', methods=['POST'])
def add_form():
    form = request.form
    print form
    response = make_response(jsonify({"code": 0}))
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Request-Method'] = 'OPTIONS, HEAD, GET'
    return response