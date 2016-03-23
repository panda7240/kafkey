#!/usr/bin/env python
# -*- coding: utf8 -*-
import json
import unittest
import time
from app import create_app
import app
from app.main.controller.message_controller import aggs_error_count

__author__ = 'panda'


class MessageTestCase(unittest.TestCase):


    def obj_to_json(self, obj):
        return json.dumps(obj, encoding='utf8', ensure_ascii=False, indent=2)


    def json_to_obj(self,json_str):
        return json.loads(json_str, encoding='utf8')


    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_es_client(self):
        self.assertTrue(app.es is not None)

    def test_query(self):
        res = app.es.search(index="kafka_msg_log_2016.03.17", body={"query": {"match_all": {}}})
        print("Got %d Hits" % res['hits']['total'])

    # 根据mid获取整个消息传递链信息
    def test_query_by_mid(self):
        res = app.es.search(
                index="kafka_msg_log_2016.03.17",
                body={
                        "from": 0,
                        "size": 10000,
                        "query": {
                            "bool": {
                                "must": {
                                    "term": {
                                        "mid": "96d223ed-203c-4807-a73d-3f3cdbecb57c"
                                    }
                                }
                            }
                        },
                        "sort": [
                            {
                                "stage": {
                                    "order": "asc"
                                }
                            }
                        ]
                     }
                )
        for obj in res['hits']['hits']:
            print self.obj_to_json(obj['_source'])

        # print("Got %d Hits" % res['hits']['total'])

    # 统计有哪些msg传递过程中缺失四个过程, 并显示这些msg最后一个环节的详细信息
    def test_aggs_broke_mid(self):
        res = app.es.search(
                index=["kafka_msg_log_2016.03.17","kafka_msg_log_2016.03.21"],
                body={
                        "from": 0,
                        "size": 10000,
                        "query": {
                            "bool": {
                                "must": {
                                    "missing": {
                                        "field": "etype"
                                    }
                                }
                            }
                        },
                        "aggs": {
                            "mid": {
                                "terms": {
                                    "field": "mid",
                                    "size": 10000
                                    # "min_doc_count": 3
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
                        }
                    }
                )
        count = 0
        for obj in res['aggregations']['mid']['buckets']:
            if obj['doc_count'] < 4 :
                count = count + 1
                last_log = obj['last_msg']['hits']['hits'][0]['_source']
                timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(last_log['timestamp']) / 1000))
                print 'mid: [' + last_log['mid'] + ']  count: [' + str(obj['doc_count']) + ']  time: [' + timestamp + ']  stage: [' + str(last_log['stage']) + ']'
            # print self.obj_to_json(obj)
        print 'count: [' + str(count) + ']'




    # 统计一天范围内所有错误的异常
    def test_aggs_error(self):
        topic_name = None
        group_name = None
        app_name = None
        ip = None
        time_scope = 72

        aggs_error_count(topic_name, group_name, app_name, ip, time_scope)

