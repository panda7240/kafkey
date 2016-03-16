# -*- coding:utf-8 -*-

from app import db
from app.main.controller import login_required
from flask import render_template, session, redirect, url_for, current_app, request, Blueprint

kafka_blueprint = Blueprint('kafka_blueprint', __name__)


@kafka_blueprint.route('/cluster/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('cluster/index.html')



@kafka_blueprint.route('/cluster/simplelist', methods=['GET', 'POST'])
@login_required
def query_simple():
