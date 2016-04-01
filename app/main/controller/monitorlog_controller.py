# -*- coding:utf-8 -*-
import json
import time
import app
from app.main.controller import login_required
from elasticsearch.client import IndicesClient
from flask import render_template, session, redirect, url_for, current_app, request, Blueprint

monitorlog_blueprint = Blueprint('monitorlog_blueprint', __name__)


@monitorlog_blueprint.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    timestamp = request.values.get("timestamp")
    etype = request.values.get("etype")
    if timestamp==None:
        timestamp=""
    if etype == None:
        etype = ""
    return render_template('monitorlog/index.html', etype=etype, timestamp=timestamp)


@monitorlog_blueprint.route('/detailpage', methods=['GET', 'POST'])
@login_required
def detailpage():
    mid = request.values.get("mid")
    timestamp = request.values.get("timestamp")
    if timestamp==None:
        timestamp=""

    return render_template('monitorlog/detail.html', mid=mid, timestamp=timestamp)


@monitorlog_blueprint.route('/getdata', methods=['GET', 'POST'])
@login_required
def getdata():
    arg_dict = request.values

    timestamp = request.values["timestamp"]

    res = get_need_datas(get_indexs(timestamp), arg_dict.__dict__["dicts"][1], 10)

    # print json.dumps(res, encoding='utf8', ensure_ascii=False, indent=2)

    return json.dumps(res, encoding='utf8', ensure_ascii=False, indent=2)


@monitorlog_blueprint.route('/detail', methods=['GET', 'POST'])
@login_required
def detail():
    arg_dict = request.values

    timestamp = request.values["timestamp"]

    res = get_need_detail_datas(get_indexs(timestamp), arg_dict.__dict__["dicts"][1], 10)

    # print json.dumps(res, encoding='utf8', ensure_ascii=False, indent=2)

    return json.dumps(res, encoding='utf8', ensure_ascii=False, indent=2)


def get_indexs(msvalue):
    return "kafka_msg_log_" + time.strftime("%Y.%m.%d", time.localtime(long(msvalue) / 1000))


def gen_musts(arr):
    req = []
    if arr.has_key("mid") and arr.get("mid"):
        req.append({"match": {"mid": arr["mid"]}})
    if arr.has_key("app") and arr.get("app"):
        req.append({"match": {"app": arr["app"]}})
    if arr.has_key("host") and arr.get("host"):
        req.append({"match": {"host": arr["host"]}})
    if arr.has_key("ip") and arr.get("ip"):
        req.append({"match": {"ip": arr["ip"]}})
    if arr.has_key("topic") and arr.get("topic"):
        req.append({"match": {"topic": arr["topic"]}})
    if arr.has_key("pid") and arr.get("pid"):
        req.append({"match": {"pid": int(arr["pid"])}})

    if arr.has_key("group") and arr.get("group"):
        req.append({"match": {"group": arr["group"]}})
    if arr.has_key("partition") and arr.get("partition"):
        req.append({"match": {"partition": int(arr["partition"])}})
    if arr.has_key("offset") and arr.get("offset"):
        req.append({"match": {"offset": long(arr["offset"])}})

    if arr.has_key("etype") and arr.get("etype"):
        req.append({"match": {"etype": int(arr["etype"])}})
    if arr.has_key("stage") and arr.get("stage"):
        req.append({"match": {"stage": int(arr["stage"])}})

    min_num = 10
    if arr.has_key("mins") and arr.get("mins"):
        min_num = int(arr["mins"])

    if arr.has_key("timestamp"):
        timestamp = long(arr["timestamp"])
        req.append({"range": {"timestamp": {
            "gte": timestamp - min_num * 1000 * 60,
            "lte": timestamp
        }}})

    return req


def get_need_datas(indexs, arg_dict, size=10):
    gen_musts(arg_dict)

    body = {
        "from": 0,
        "size": 0,
        'query': {
            "bool": {
                "must": gen_musts(arg_dict),
            }
        },
        "fields": "mid",
        "aggregations": {
            "mid": {
                "terms": {
                    "field": "mid",
                    "size": size,
                    # "sort": [
                    #             {
                    #                 "timestamp": {
                    #                     "order": "desc"
                    #                 }
                    #             }
                    #         ]
                },
                # "sort": [
                #     {
                #         "timestamp": {
                #             "order": "desc"
                #         }
                #     }
                # ],
                "aggs": {
                    "last_msg": {
                        "top_hits": {
                            "size": 1,
                            "sort": [
                                {
                                    "stage": {
                                        "order": "desc"
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        },
        "sort": [
            {
                "timestamp": {
                    "order": "desc"
                }
            }
        ]
    }

    result = app.es.search(
        ignore=404,
        index=indexs,
        body=body
    )
    req = []
    # if result["status"] == 200 :
    for r in result['aggregations']['mid']['buckets']:
        try:
            req.append(r["last_msg"]["hits"]["hits"][0]["_source"])
        except:
            pass

    return req

def get_need_detail_datas(indexs, arg_dict, size=1000):
    gen_musts(arg_dict)

    body = {
        "from": 0,
        "size": size,
        'query': {
            "bool": {
                "must": gen_musts(arg_dict),
            }
        },
        "sort": [
            {
                "timestamp": {
                    "order": "asc"
                }
            }
        ]
    }

    result = app.es.search(
        ignore=404,
        index=indexs,
        body=body
    )
    req = []
    for r in result['hits']['hits']:
        try:
            req.append(r["_source"])
        except:
            pass

    return req
