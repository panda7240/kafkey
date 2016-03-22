# -*- coding:utf-8 -*-
import time
import app
from app.main.controller import login_required
from elasticsearch.client import IndicesClient
from flask import render_template, session, redirect, url_for, current_app, request, Blueprint

message_blueprint = Blueprint('message_blueprint', __name__)



@message_blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('message/index.html')


@message_blueprint.route('/error_stat', methods=['GET', 'POST'])
@login_required
def error_stat():
    topic_name = request.values.get('topic_name')
    group_name = request.values.get('group_name')
    app_name = request.values.get('app_name')
    ip = request.values.get('ip')
    return render_template('message/error_stat.html', topic_name=topic_name, group_name=group_name, app_name=app_name,ip=ip)


@message_blueprint.route('/get_error_stat', methods=['GET', 'POST'])
@login_required
def get_error_stat():
    time_scope = request.values.get('time_scope')
    topic_name = request.values.get('topic_name')
    group_name = request.values.get('group_name')
    app_name = request.values.get('app_name')
    ip = request.values.get('ip')
    return render_template('message/error_stat.html')







# 统计一天范围内所有错误的异常
def aggs_error_count(topic_name, group_name, app_name, ip, time_scope=1):
    index_list = []
    # 根据检索范围获取索引名称, 并验证索引是否存在, 并生成已经存在的索引列表
    indicesClient = IndicesClient(app.es)
    for count in range((time_scope/24)+1):
        index_name = 'kafka_msg_log_' + time.strftime('%Y.%m.%d', time.localtime(time.time() - int(count)*24*60*60))
        if indicesClient.exists(index_name):
            index_list.append(index_name)
    if index_list.__len__() == 0:
        return

    start_time = "now-" + str(time_scope) + "h/h"

    must_terms = []
    group_dict = None
    if group_name:
        group_dict = {
                        "match": {
                            "group": {
                                "query": group_name,
                                "type": "phrase"
                            }
                        }
                    }
        must_terms.append(group_dict)

    topic_dict = None
    if topic_name:
        topic_dict = {
                        "match": {
                            "topic": {
                                "query": topic_name,
                                "type": "phrase"
                            }
                        }
                    }
        must_terms.append(topic_dict)

    app_dict = None
    if app_name:
        app_dict = {
                    "match": {
                        "app": {
                            "query": app_name,
                            "type": "phrase"
                        }
                    }
                }
        must_terms.append(app_dict)

    ip_dict = None
    if ip:
        ip_dict = {
                    "match": {
                        "ip": {
                            "query": ip,
                            "type": "phrase"
                        }
                    }
                }
        must_terms.append(ip_dict)

    res = app.es.search(
            index=index_list,
            body={
                    "from": 0,
                    "size": 10000,
                    "query": {
                        "bool": {
                            "must_not": {
                                "missing": {
                                    "field": "etype"
                                }
                            },
                            "must": must_terms
                        }
                    },
                    "aggs" : {
                        "error_count" : {
                            "date_histogram" : {
                                "field" : "timestamp",
                                "interval" : "10m",
                                "format" : "yyyy-MM-dd HH:mm",
                                "min_doc_count": 0
                            }
                        }
                    }
                }
            )
    for obj in res['aggregations']['error_count']['buckets']:
        print 'datetime: [' + obj['key_as_string'] + ']  count: [' + str(obj['doc_count']) + ']'

