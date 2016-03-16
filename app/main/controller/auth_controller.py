# -*- coding:utf-8 -*-
import logging
from app.main.controller import login_required
from app.main.model.user import User
from flask import render_template, session, redirect, url_for, current_app, request, Blueprint

auth_blueprint = Blueprint('auth_blueprint', __name__)

logger = logging.getLogger('auth_controller')

@auth_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', username = session.get("user"))



@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    userName = request.values.get('user_account')
    password = request.values.get('user_pwd')

    if userName is not None and password is not None:
        user = User.query.filter_by(name=userName).first()
        if user is not None and user.verify_password(password):
            session['user'] = userName
            logger.info(userName + ' sign in successfully !')
            return 'SUCCESS'
    else:
        return render_template('login.html')


@auth_blueprint.route('/logout')
def logout():
    session['user'] = None
    return redirect("/")



