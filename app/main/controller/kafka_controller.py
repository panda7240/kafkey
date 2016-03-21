# -*- coding:utf-8 -*-
import time
from app import db
from app.main import is_ip_port

from app.main.controller import login_required, json_result
from app.main.model.cluster import Cluster
from flask import render_template, Blueprint, request
from kazoo.client import KazooClient

kafka_blueprint = Blueprint('kafka_blueprint', __name__)


@kafka_blueprint.route('/cluster/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('cluster/index.html')


@kafka_blueprint.route('/cluster/simplelist', methods=['GET', 'POST'])
@login_required
def query_simple():
    query = Cluster.query.order_by(Cluster.name.asc())
    rows = [get_zk_info(c) for c in query.all()]
    return json_result(query.count(), rows)


# 获取broker的topic数量信息
def get_zk_info(cluster):
    try:
        zk = KazooClient(hosts=cluster.zookeeper, )
        zk.start()
        topics = zk.get_children('/brokers/topics/')
        brokers = zk.get_children('/brokers/ids/')
        cluster.other_dict = {'topic_num': len(topics), 'broker_num': len(brokers)}
        return cluster
    finally:
        zk.stop()
        zk.close()


@kafka_blueprint.route('/cluster/add', methods=['POST', 'GET'])
@login_required
def add():
    return add_cluster()


@kafka_blueprint.route('/cluster/update', methods=['POST', 'GET'])
@login_required
def update():
    cluster_id = request.values.get('id')
    if cluster_id is None:
        return 'parameter {id} exception'
    cluster = Cluster.query.filter(Cluster.id == cluster_id).first()
    if cluster is None:
        return 'id not exit'
    else:
        return add_cluster(cluster)


def add_cluster(cluster=None):
    name = request.values.get('name')
    broker = request.values.get('broker')
    zookeeper = request.values.get('zookeeper')
    remark = request.values.get('remark')
    if name is None or name == '':
        return 'parameter {name} exception'
    if broker is None or broker == '':
        return 'parameter {broker} exception'
    if zookeeper is None or zookeeper == '':
        return 'parameter {zookeeper} exception'
    if False in map(is_ip_port, broker.split(',')):
        return 'parameter {broker} illegal'
    if False in map(is_ip_port, zookeeper.split(',')):
        return 'parameter {zookeeper} illegal'
    if cluster is None:
        cluster = Cluster(create_time=time.strftime('%Y-%m-%d %X', time.localtime()))
    cluster.name = name
    cluster.broker = broker
    cluster.zookeeper = zookeeper
    cluster.remark = remark
    db.session.add(cluster)
    return 'SUCCESS'


@kafka_blueprint.route('/cluster/delete', methods=['POST', 'GET'])
@login_required
def delete():
    id = request.values.get('id')
    if id is None:
        return 'parameter {id} exception'
    cluster = Cluster.query.filter(Cluster.id == id).first()
    if cluster is not None:
        db.session.delete(cluster)
        return 'SUCCESS'
    else:
        return 'id not exit'
