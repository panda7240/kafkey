#!/usr/bin/env python
# -*- coding: utf8 -*-
import unittest
from app import create_app, es

__author__ = 'panda'


class MessageTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_es_client(self):
        self.assertTrue(es is not None)
