# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask import render_template, request, jsonify

from service import LoginTypeService
from webapp.views.login_type import blueprint


@blueprint.route('/all')
def get_all():
    all_lt = LoginTypeService.all()
    return jsonify(all_lt)


@blueprint.route('/list')
def get_list():
    page = int(request.args.get('page', 1))
    size = int(request.args.get('limit', 20))
    lt = request.args.get('type', None)
    lt_list = LoginTypeService.get_list(lt, page, size)
    lt_list.update({'code': 0})
    return jsonify(lt_list)


@blueprint.route('/')
def index():
    return render_template('logintype/list.html')


@blueprint.route('/add', methods=['GET'])
def add():
    ft = '添加'
    return render_template('logintype/form.html',
                           form_url='/server/login/type/form/add',
                           form_type=ft)


@blueprint.route('/form/add', methods=['GET', 'POST'])
def add_form():
    form = request.form
    LoginTypeService.save(name=form.get('name'))
    return jsonify({'code': 0})


@blueprint.route('/edit', methods=['GET'])
def edit():
    ft = '编辑'
    _id = int(request.args.get('id'))
    lt = LoginTypeService.get_by_id(_id)
    return render_template('logintype/form.html',
                           form_url='/server/login/type/form/edit',
                           form_type=ft, **lt)


@blueprint.route('/form/edit', methods=['GET', 'POST'])
def edit_form():
    form = request.form
    LoginTypeService.alert(_id=form.get('id'), name=form.get('name'))
    return jsonify({'code': 0})


@blueprint.route('/form/delete', methods=['GET', 'POST'])
def delete_by_id():
    _id = str(request.args.get('ids'))
    ids = _id.split(',')
    LoginTypeService.delete_by_ids(ids)
    return jsonify({'code': 0})
