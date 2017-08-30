# -*- coding:utf-8 -*-


import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from webapp.views.inventory import blueprint
from flask import render_template, request, jsonify
from webapp.views.server_group.service import ServerGroupService
from webapp.views.inventory.service import InventoryService


@blueprint.route('/inventory', methods=['GET'])
def index():
    server_groups = ServerGroupService.get_all()
    return render_template('inventory/list.html', group_list=server_groups)


@blueprint.route('/inventory/list', methods=['GET', 'POST'])
def get_page_list():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('limit', 20))
    inventory = {}
    if request.args.get('name'):
        inventory['name'] = request.args.get('name')
    if request.args.get('group'):
        inventory['group_id'] = request.args.get('group')
    inventory_list = InventoryService.get_list(inventory, page, size)
    inventory_list.update({'code': 0})
    return jsonify(inventory_list)


@blueprint.route('/inventory/add', methods=['POST', 'GET'])
def add():
    ft = '添加'
    server_groups = ServerGroupService.get_all()
    return render_template('inventory/form.html',
                           form_url='/inventory/form/add',
                           form_type=ft,
                           server_group_list=server_groups)


@blueprint.route('/inventory/form/add', methods=['POST'])
def add_form():
    form = request.form
    result = InventoryService.add(name=form.get('name'),
                                  group_id=form.get('group_id') if form.get('group_id') else None,
                                  memo=form.get('memo'))
    if result:
        return jsonify({'code': 0})
    else:
        return jsonify({'code': -1})


@blueprint.route('/inventory/edit', methods=['POST'])
def edit():
    _id = int(request.args.get('id'))
    ft = '修改'
    server_groups = ServerGroupService.get_all()
    inventory = InventoryService.get_by_id(_id)
    return render_template('inventory/form.html',
                           form_url='/inventory/form/edit',
                           form_type=ft,
                           server_group_list=server_groups,
                           **inventory)


@blueprint.route('/inventory/form/edit', methods=['POST'])
def edit_form():
    form = request.form
    InventoryService.alert(_id=form.get('id'),
                           name=form.get('name'),
                           group_id=form.get('group_id'),
                           memo=form.get('memo'))
    return jsonify({'code': 0})


@blueprint.route('/inventory/form/delete', methods=['GET', 'POST'])
def delete_by_id():
    _id = str(request.args.get('ids'))
    ids = _id.split(',')
    InventoryService.delete_by_ids(ids)
    return jsonify({'code': 0})
