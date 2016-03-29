# -*- coding:utf-8 -*-


from elasticsearch import Elasticsearch
import json
import time


def dict_to_json(dic):
    return json.dumps(dic, encoding='utf8', ensure_ascii=False, indent=2)


def json_to_dict(jstr):
    return json.loads(jstr, encoding='utf8')


es = Elasticsearch(
    hosts='192.168.10.235',
    port=9200,
)

'''
两步检索, first : mid , second, 链条结构

1 bool 条件 : mid, errtype, group  topic  ip  host pid  app partition offset timestamp

2 根据mid检索
'''


def gen_musts(arr):
    req = []
    if arr.has_key("mid"):
        req.append({"match": {"mid": arr["mid"]}})
    if arr.has_key("app"):
        req.append({"match": {"app": arr["app"]}})
    if arr.has_key("host"):
        req.append({"match": {"host": arr["host"]}})
    if arr.has_key("ip"):
        req.append({"match": {"ip": arr["ip"]}})
    if arr.has_key("topic"):
        req.append({"match": {"topic": arr["topic"]}})
    if arr.has_key("pid"):
        req.append({"match": {"pid": int(arr["pid"])}})

    if arr.has_key("group"):
        req.append({"match": {"group": arr["group"]}})
    if arr.has_key("partition"):
        req.append({"match": {"partition": int(arr["partition"])}})
    if arr.has_key("offset"):
        req.append({"match": {"offset": long(arr["offset"])}})

    if arr.has_key("etype"):
        req.append({"match": {"etype": int(arr["etype"])}})
    if arr.has_key("stage"):
        req.append({"match": {"stage": int(arr["stage"])}})

    min_num = 10
    if arr.has_key("min_num"):
        min_num = int(arr["stage"])

    if arr.has_key("timestamp"):
        timestamp = long(arr["timestamp"])
        req.append({"range": {"timestamp": {
            "gte": timestamp - min_num * 1000 * 60,
            "lte": timestamp
        }}})

    return req


def get_need_mids(arg_dict, size):
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
                    "size": size
                },
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
    result = es.search(
        index='kafka_msg_log_2016.03.23',
        body=body
    )

    print dict_to_json(result)

    req = []
    for r in result['aggregations']['mid']['buckets']:
        # req.append(r['key'])
        req.append(r["last_msg"]["hits"]["hits"][0]["_source"])

    return req


print get_need_mids({}, 10)


def get_data(mid_list):
    pass
