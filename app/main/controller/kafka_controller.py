# -*- coding:utf-8 -*-

from app.main.controller import login_required, json_result
from app.main.model.cluster import Cluster
from flask import render_template, Blueprint

kafka_blueprint = Blueprint('kafka_blueprint', __name__)


@kafka_blueprint.route('/cluster/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('cluster/index.html')


@kafka_blueprint.route('/cluster/simplelist', methods=['GET', 'POST'])
@login_required
def query_simple():
    query = Cluster.query.order_by(Cluster.name.asc())
    return json_result(query.count(), query.all())
