# -*- coding:utf-8 -*-
from app.main.controller import login_required
from flask import render_template, session, redirect, url_for, current_app, request, Blueprint

message_blueprint = Blueprint('message_blueprint', __name__)



@message_blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('message/index.html')


