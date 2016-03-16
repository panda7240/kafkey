# -*- coding:utf-8 -*-

from app.main.controller import login_required
from app.main.model.json_result import JsonResult
from app.main.model.user import User
from flask import render_template, Blueprint

kafka_blueprint = Blueprint('kafka_blueprint', __name__)


@kafka_blueprint.route('/cluster/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('cluster/index.html')


@kafka_blueprint.route('/cluster/simplelist', methods=['GET', 'POST'])
@login_required
def query_simple():
    query = User.query.order_by(User.name.asc())
    total = query.count()
    rows = query.all()
    return str(JsonResult(total, rows))
