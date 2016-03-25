# -*- coding:utf-8 -*-
import json
import time
from app import db
from app.main import is_ip_port

from app.main.controller import login_required, json_result
from app.main.model.cluster import Cluster
from app.main.model.cluster_zookeeper import ClusterZookeeper
from flask import render_template, Blueprint, request
from kazoo.handlers.threading import KazooTimeoutError

kafka_blueprint = Blueprint('kafka_blueprint', __name__)

zk_dict = {}


@kafka_blueprint.before_app_first_request
def run_on_start():
    clusters = Cluster.query.all()
    map(start_watch, clusters)


def start_watch(cluster):
    try:
        zk_dict[cluster.id] = ClusterZookeeper(cluster.zookeeper)
        return 'SUCCESS'
    except KazooTimeoutError as e:
        return cluster.zookeeper + e.message
    except ValueError as e:
        return e.message


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
    if cluster.id in zk_dict:
        cluster.other_dict = {'topic_num': len(zk_dict[cluster.id].topics_dict),
                              'broker_num': len(zk_dict[cluster.id].brokers_list)}
    return cluster


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
        return add(cluster)


@kafka_blueprint.route('/cluster/add', methods=['POST', 'GET'])
@login_required
def add(cluster=None):
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
    must_re_watch = False
    if cluster is None:
        cluster = Cluster(create_time=time.strftime('%Y-%m-%d %X', time.localtime()))
        must_re_watch = True
    elif zookeeper != cluster.zookeeper:
        must_re_watch = True
    cluster.name = name
    cluster.broker = broker
    cluster.zookeeper = zookeeper
    cluster.remark = remark
    db.session.add(cluster)
    if must_re_watch:
        db.session.flush()
        res = start_watch(cluster)
        if res != 'SUCCESS':
            db.session.rollback()
            return res
    return 'SUCCESS'


@kafka_blueprint.route('/cluster/delete', methods=['POST', 'GET'])
@login_required
def delete():
    cluster_id = request.values.get('id')
    if cluster_id is None:
        return 'parameter {id} exception'
    cluster = Cluster.query.filter(Cluster.id == cluster_id).first()
    if cluster is not None:
        if cluster.id in zk_dict:
            zk_dict[cluster.id].close_zk()
            zk_dict.pop(cluster.id)
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
    page = int(request.values.get('page'))
    rows = int(request.values.get('rows'))
    search_str = request.values.get('sSearch')
    cluster = get_cluster(cluster_id)
    if cluster is None:
        raise TypeError("Invalid type for 'cluster_id' (no data)")
    # 计算topic的消费者分组
    topic_groups = get_topic_groups(cluster.id)
    topics_dict = zk_dict[cluster.id].topics_dict
    res_list = []
    for topic, value in topics_dict.items():
        partitions = value.topic_value
        s1 = set([])
        for k, v in partitions.items():
            rep_num = len(v)
            s1 = s1 | set(v)
        groups = topic_groups.get(topic, [])
        if search_str is None:
            res_list.append({"topic_name": topic, "partition_num": len(partitions), "rep_num": rep_num,
                             "broker_num": len(s1), 'group_num': len(groups), 'groups_str': ','.join(groups)})
        elif topic.find(search_str) > -1:
            res_list.append({"topic_name": topic, "partition_num": len(partitions), "rep_num": rep_num,
                             "broker_num": len(s1), 'group_num': len(groups), 'groups_str': ','.join(groups)})
    start = (page - 1) * rows
    return json_result(len(res_list), res_list[start:min(start + rows, len(res_list))])


def get_topic_groups(cluster_id):
    groups_dict = zk_dict[cluster_id].groups_dict
    topic_groups = {}
    for g, v in groups_dict.items():
        for g_topic in v.topics_list:
            topic_groups[g_topic] = topic_groups.get(g_topic, []) + [g]
    return topic_groups


################################################################################################################


@kafka_blueprint.route('/group/index', methods=['GET', 'POST'])
@login_required
def group_index():
    cluster_id = request.values.get('cluster_id')
    topic_name = request.values.get('topic_name')
    groups_str = request.values.get('groups_str')
    return render_template('group/index.html', topic_name=topic_name, cluster_id=cluster_id, groups_str=groups_str)


@kafka_blueprint.route('/group/list', methods=['GET', 'POST'])
@login_required
def group_list():
    cluster_id = request.values.get('cluster_id')
    groups_str = request.values.get('groups_str')
    cluster = get_cluster(cluster_id)
    if cluster is None:
        raise TypeError("Invalid type for 'cluster_id' (no data)")
    topic_name = request.values.get('topic_name')
    res_list = []
    for group in groups_str.split(','):
        if zk_dict[cluster.id].zk.exists('/consumers/' + group + '/owners/' + topic_name) is None:
            continue
        partitions = zk_dict[cluster.id].zk.get_children('/consumers/' + group + '/owners/' + topic_name)
        p_dict = {}
        for partition in partitions:
            c_data = zk_dict[cluster.id].zk.get('/consumers/' + group + '/owners/' + topic_name + '/' + partition)
            c_name = c_data[0][:c_data[0].rfind('-')]
            p_dict[c_name] = [partition] + p_dict.get(c_name, [])
        for k, v in p_dict.items():
            res_list.append({"group_name": group, "consumer": k, "partition": ",".join(v)})
    return json.dumps(res_list)
