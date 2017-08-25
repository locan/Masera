# -*- coding:utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from flask import render_template, request, jsonify
from webapp.views.server_group import blueprint
from webapp.views.server_group.service import ServerGroupService


@blueprint.route('/server/group', methods=['GET'])
def index():
    return render_template('group/list.html')


@blueprint.route('/server/group/list', methods=['GET', 'POST'])
def get_page_list():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('limit', 20))
    group = request.args.get('group', None)
    group_list = ServerGroupService.get_list(group, page, size)
    group_list.update({'code': 0})
    return jsonify(group_list)


@blueprint.route('/server/group/add', methods=['GET'])
def add():
    ft = '添加'
    return render_template('group/form.html',
                           form_url='/server/group/form/add',
                           form_type=ft)


@blueprint.route('/server/group/form/add', methods=['GET', 'POST'])
def add_form():
    form = request.form
    ServerGroupService.add(name=form.get('name'),
                           memo=form.get('memo'))
    return jsonify({'code': 0})


@blueprint.route('/server/group/edit', methods=['GET'])
def edit():
    ft = '编辑'
    _id = int(request.args.get('id'))
    g = ServerGroupService.get_by_id(_id)
    return render_template('group/form.html',
                           form_url='/server/group/form/edit',
                           form_type=ft, **g)


@blueprint.route('/server/group/form/edit', methods=['GET', 'POST'])
def edit_form():
    form = request.form
    ServerGroupService.alert(_id=form.get('id'),
                             name=form.get('name'),
                             memo=form.get('memo'))
    return jsonify({'code': 0})


@blueprint.route('/server/group/form/delete', methods=['GET', 'POST'])
def delete_by_id():
    _id = str(request.args.get('ids'))
    ids = _id.split(',')
    ServerGroupService.delete_by_ids(ids)
    return jsonify({'code': 0})
