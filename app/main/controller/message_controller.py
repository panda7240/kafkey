# -*- coding:utf-8 -*-
import json
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
    return aggs_error_count(topic_name, group_name, app_name, ip, time_scope)







# 统计n小时范围内所有错误的异常
def aggs_error_count(topic_name, group_name, app_name, ip, time_scope=1):
    index_list = []
    # 根据检索范围获取索引名称, 并验证索引是否存在, 并生成已经存在的索引列表
    indicesClient = IndicesClient(app.es)
    for count in range((int(time_scope)/24)+1):
        index_name = 'kafka_msg_log_' + time.strftime('%Y.%m.%d', time.localtime(time.time() - int(count)*24*60*60))
        if indicesClient.exists(index_name):
            index_list.append(index_name)
    if index_list.__len__() == 0:
        return

    start_time = "now-" + str(time_scope) + "h/h"
    range_dict = {
                    "range" : {
                        "timestamp" : {
                            "gte" : start_time,
                            "lte" :  "now/h"
                        }
                    }
                }

    must_list = _assemble_must_terms(topic_name, group_name, app_name, ip)
    must_list.append(range_dict)
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
                            "must": must_list
                        }
                    },
                    "fields": "etype",
                    "aggregations": {
                        "aggs": {
                            "date_histogram": {
                                "field": "timestamp",
                                "interval": "10m",
                                "format": "yyyy-MM-dd HH:mm",
                                "time_zone": "+08:00",
                                "min_doc_count": 0
                            },
                            "aggregations": {
                                "etype": {
                                    "terms": {
                                        "field": "etype",
                                        "min_doc_count": 0,
                                        "size": 10000
                                    },
                                    "aggregations": {
                                        "etype_count": {
                                            "value_count": {
                                                "field": "etype"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            )

    xAxis = set([])
    error_stat_dict = {}
    for obj in res['aggregations']['aggs']['buckets']:
        date_time = obj['key_as_string']
        xAxis.add(date_time)
        # 添加横坐标列表
        etype_count_aggs = obj['etype']['buckets']
        for etype_count_obj in etype_count_aggs:
            etype_count = etype_count_obj['etype_count']['value']
            etype = etype_count_obj['key']

            if date_time not in error_stat_dict:
                error_stat_dict[date_time] = [{"etype":etype, "count":etype_count}]
            else:
                temp_list = error_stat_dict[date_time]
                temp_list.append({"etype":etype, "count":etype_count})
                error_stat_dict[date_time] = temp_list

            # error_stat_result.append(error_stat_dict)
            print 'etype:[' + str(etype) + ']  datetime: [' + date_time + ']  count: [' + str(etype_count) + ']'
    xAxis = sorted(xAxis)

    # 发送异常数据集
    send_error_list = []
    # 业务异常数据集
    business_error_list = []
    for x_date_time in xAxis:
        temp_etype_dict_list = error_stat_dict[x_date_time]
        if temp_etype_dict_list:
            for etype_dict in temp_etype_dict_list:
                if etype_dict['etype'] == 1:
                    send_error_list.append(etype_dict['count'])
                else:
                    business_error_list.append(etype_dict['count'])

    error_stat_result = {
        "xAxis": xAxis,
        "send_error_list": send_error_list,
        "business_error_list": business_error_list,
        "success": "true",
        "group_name": group_name,
        "topic_name": topic_name,
        "app_name": app_name,
        "ip": ip
    }
    return json.dumps(error_stat_result, encoding='utf8', ensure_ascii=False, indent=2)


# 组装检索条件, 返回must数组
def _assemble_must_terms(topic_name, group_name, app_name, ip):
    must_terms = []
    if group_name and group_name != "None":
        group_dict = {
                        "match": {
                            "group": {
                                "query": group_name,
                                "type": "phrase"
                            }
                        }
                    }
        must_terms.append(group_dict)

    if topic_name and topic_name != "None":
        topic_dict = {
                        "match": {
                            "topic": {
                                "query": topic_name,
                                "type": "phrase"
                            }
                        }
                    }
        must_terms.append(topic_dict)

    if app_name and app_name != "None":
        app_dict = {
                    "match": {
                        "app": {
                            "query": app_name,
                            "type": "phrase"
                        }
                    }
                }
        must_terms.append(app_dict)

    if ip and ip != "None":
        ip_dict = {
                    "match": {
                        "ip": {
                            "query": ip,
                            "type": "phrase"
                        }
                    }
                }
        must_terms.append(ip_dict)
    return must_terms