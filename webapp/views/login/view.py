# -*- coding:utf-8 -*-
from flask import render_template, request, redirect, url_for

from webapp.login_form import LoginForm
from webapp.views.login import blueprint

from webapp.models import User
from flask_login import login_user, logout_user


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me', False)
        user_obj = User()
        user = user_obj.get_by_username(user_name)
        if user.verify_password(password) and login_user(user, remember=remember_me):
            # print request.args.get('next')
            return redirect(request.args.get('next') or url_for('webapp.views.server.index'))

    return render_template('login.html', title="Sign In", form=form)


@blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('.login'))
