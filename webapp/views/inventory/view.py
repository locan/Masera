# -*- coding:utf-8 -*-


import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from webapp.views.inventory import blueprint
from flask import render_template, request, jsonify
from webapp.views.server_group.service import ServerGroupService
from webapp.views.inventory.service import InventoryService, InventoryGroupService


@blueprint.route('/', methods=['GET'])
def index():
    server_groups = ServerGroupService.get_all()
    return render_template('inventory/list.html', group_list=server_groups)


@blueprint.route('/list', methods=['GET', 'POST'])
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


@blueprint.route('/add', methods=['POST', 'GET'])
def add():
    ft = '添加'
    server_groups = ServerGroupService.get_all()
    return render_template('inventory/form.html',
                           form_url='/inventory/form/add',
                           form_type=ft,
                           server_group_list=server_groups)


@blueprint.route('/form/add', methods=['POST'])
def add_form():
    form = request.form
    result = InventoryService.add(name=form.get('name'),
                                  group_id=form.get('group_id') if form.get('group_id') else None,
                                  memo=form.get('memo'))
    if result:
        return jsonify({'code': 0})
    else:
        return jsonify({'code': -1})


@blueprint.route('/edit', methods=['POST'])
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


@blueprint.route('/form/edit', methods=['POST'])
def edit_form():
    form = request.form
    InventoryService.alert(_id=form.get('id'),
                           name=form.get('name'),
                           group_id=form.get('group_id'),
                           memo=form.get('memo'))
    return jsonify({'code': 0})


@blueprint.route('/form/delete', methods=['GET', 'POST'])
def delete_by_id():
    _id = str(request.args.get('ids'))
    ids = _id.split(',')
    InventoryService.delete_by_ids(ids)
    return jsonify({'code': 0})


@blueprint.route('/detail', methods=['GET', 'POST'])
def inventory_detail():
    _id = int(request.args.get('id'))
    inventory = InventoryService.get_by_id(_id).to_dict()
    return render_template('inventory/inventory_group_host.html', **inventory)


@blueprint.route('/group/add')
def inventory_group():
    inventory_id = request.args.get('inventoryid')
    server_groups = ServerGroupService.get_all()
    return render_template('inventory/form_group.html',
                           form_type='添加',
                           server_group_list=server_groups,
                           inventory_id=inventory_id,
                           form_url='/inventory/group/form/add')


@blueprint.route('/group/form/add', methods=['POST', 'GET'])
def inventory_group_add_form():
    form = request.form
    inventory_id = form.get('inventory_id')
    group_id = form.get('group_id')
    name = form.get('name')
    memo = form.get('memo')
    igs = InventoryGroupService.add(name, group_id, inventory_id, memo)
    if igs:
        return jsonify({'code': 0})
    else:
        return jsonify({'code': -1})


@blueprint.route('/group/form/edit', methods=['POST', 'GET'])
def inventory_group_edit_form():
    form = request.form
    inventory_id = form.get('inventory_id')
    group_id = form.get('group_id')
    name = form.get('name')
    memo = form.get('memo')
    _id = form.get('id')
    igs = InventoryGroupService.alter(_id, name, group_id, inventory_id, memo)
    if igs:
        return jsonify({'code': 0})
    else:
        return jsonify({'code': -1})


@blueprint.route('/group/form/delete', methods=['POST', 'GET'])
def inventory_group_delete():
    _id = str(request.args.get('ids'))
    ids = _id.split(',')
    InventoryGroupService.delete_by_ids(ids)
    return jsonify({'code': 0})


@blueprint.route('/group/list')
def inventory_group_get_list():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('limit', 20))
    inventory_server_group = dict()
    if request.args.get('inventory_id'):
        inventory_server_group['inventory_id'] = request.args.get('inventory_id')
    if request.args.get('group_id'):
        inventory_server_group['group_id'] = request.args.get('group_id')
    if request.args.get('name'):
        inventory_server_group['name'] = request.args.get('name')

    ig_list = InventoryGroupService.get_list(inventory_server_group, page, size)
    ig_list.update({'code': 0})
    return jsonify(ig_list)


@blueprint.route('/host/add')
def inventory_host_add():
    form = request.form
    host = form.get('host')
    port = form.get('port')
    ansible_ssh_user = form.get('ansible_ssh_user')
    ansible_ssh_pass = form.get('ansible_ssh_pass')
    server_id = form.get('server_id')
    inventory_group_id = form.get('inventory_group_id')
