# -*- coding:utf-8 -*-
from flask import jsonify

from service import LoginTypeService
from webapp.views.login_type import blueprint


@blueprint.route('/login/type/all')
def get_all():
    all_lt = LoginTypeService.all()
    return jsonify(all_lt)
