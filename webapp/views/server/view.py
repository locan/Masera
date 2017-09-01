# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, request, jsonify
from service import ServerService
from webapp.views.server import blueprint
from webapp.views.login_type.service import LoginTypeService
from webapp.views.server_group.service import ServerGroupService


@blueprint.route('/', methods=['GET'])
@blueprint.route('/server', methods=['GET'])
@blueprint.route('/server/index', methods=['GET'])
def index():
    server_groups = ServerGroupService.get_all()
    return render_template('server/list.html', group_list=server_groups)


@blueprint.route('/server/list', methods=['GET', 'POST'])
def get_page_list():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('limit', 20))
    server = {}
    if request.args.get('ip'):
        server['ip'] = request.args.get('ip')
    if request.args.get('group'):
        server['group'] = request.args.get('group')
    server_list = ServerService.get_list(server, page, size)
    # return render_template('server/list.html', servers=server_list)
    server_list.update({'code': 0})
    return jsonify(server_list)


@blueprint.route('/server/add', methods=['GET'])
def add():
    ft = '添加'
    lts = LoginTypeService.get_all()
    server_groups = ServerGroupService.get_all()
    return render_template('server/form.html',
                           form_url='/server/form/add',
                           form_type=ft,
                           login_type_list=lts,
                           server_group_list=server_groups)


@blueprint.route('/server/edit', methods=['GET'])
def edit():
    _id = int(request.args.get('id'))
    ft = '修改'
    lts = LoginTypeService.get_all()
    server_groups = ServerGroupService.get_all()
    s = ServerService.get_by_id(_id)
    return render_template('server/form.html',
                           form_url='/server/form/edit',
                           form_type=ft,
                           login_type_list=lts,
                           server_group_list=server_groups, **s)


@blueprint.route('/server/form/add', methods=['POST'])
def add_form():
    form = request.form
    ServerService.add(ip=form.get('ip'),
                      group=form.get('server_group_id'),
                      purpose=form.get('purpose'),
                      deploy_server=form.get('deploy_server'),
                      position=form.get('position'),
                      login_type=form.get('login_type_id'),
                      memo=form.get('memo')
                      )

    return jsonify({'cod': 0})


@blueprint.route('/server/form/edit', methods=['POST'])
def edit_form():
    form = request.form
    ServerService.alert(_id=form.get('id'),
                        ip=form.get('ip'),
                        system_operation=form.get('system_operation'),
                        group=form.get('server_group_id'),
                        purpose=form.get('purpose'),
                        deploy_server=form.get('deploy_server'),
                        position=form.get('position'),
                        login_type=form.get('login_type_id'),
                        memo=form.get('memo')
                        )
    return jsonify({'code': 0})


@blueprint.route('/server/form/delete', methods=['GET', 'POST'])
def delete_by_id():
    _id = str(request.args.get('ids'))
    ids = _id.split(',')
    ServerService.delete_by_ids(ids)
    return jsonify({'code': 0})
