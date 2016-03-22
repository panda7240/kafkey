# -*- coding:utf-8 -*-
import json
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
        zk = KazooClient(hosts=cluster.zookeeper)
        zk.start()
        topics = zk.get_children('/brokers/topics/')
        brokers = zk.get_children('/brokers/ids/')
        cluster.other_dict = {'topic_num': len(topics), 'broker_num': len(brokers)}
        return cluster
    except Exception as e:
        print e
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
    cluster_id = request.values.get('id')
    if cluster_id is None:
        return 'parameter {id} exception'
    cluster = Cluster.query.filter(Cluster.id == cluster_id).first()
    if cluster is not None:
        db.session.delete(cluster)
        return 'SUCCESS'
    else:
        return 'id not exit'


def get_cluster(cluster_id):
    return Cluster.query.filter(Cluster.id == cluster_id).first()


################################################################################################################

@kafka_blueprint.route('/topic/index', methods=['GET', 'POST'])
@login_required
def topic_index():
    cluster_id = request.values.get('cluster_id')
    return render_template('topic/index.html', cluster_id=cluster_id)


@kafka_blueprint.route('/topic/list', methods=['GET', 'POST'])
@login_required
def topic_list():
    cluster_id = request.values.get('cluster_id')
    cluster = get_cluster(cluster_id)
    try:
        zk = KazooClient(hosts=cluster.zookeeper)
        zk.start()
        # 计算topic的消费者分组
        groups = zk.get_children('/consumers/')
        topic_dict = {}
        for group in groups:
            if zk.exists('/consumers/' + group + '/owners') is None:
                break
            group_topics = zk.get_children('/consumers/' + group + '/owners')
            for group_topic in group_topics:
                topic_dict[group_topic] = topic_dict.get(group_topic, 0) + 1

        topics = zk.get_children('/brokers/topics/')
        res_list = []
        for topic in topics:
            topic_info = zk.get('/brokers/topics/' + topic)
            partitions = json.loads(topic_info[0])["partitions"]
            s1 = set([])
            for k, v in partitions.items():
                rep_num = len(v)
                s1 = s1 | set(v)
            res_list.append({"topic_name": topic, "partition_num": len(partitions), "rep_num": rep_num,
                             "broker_num": len(s1), 'group_num': topic_dict.get(topic, 0)})
        print res_list
        return json.dumps(res_list)
    except Exception as e:
        print e
    finally:
        zk.stop()
        zk.close()
