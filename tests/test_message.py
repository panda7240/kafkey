#!/usr/bin/env python
# -*- coding: utf8 -*-
import unittest
from app import create_app
import app

__author__ = 'panda'


class MessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_es_client(self):
        self.assertTrue(app.es is not None)

    def test_query(self):
        res = app.es.search(index="eagleye_bigindex_2016.03.17", body={"query": {"match_all": {}}})
        print("Got %d Hits" % res['hits']['total'])

    def test_query_by_mid(self):
        pass