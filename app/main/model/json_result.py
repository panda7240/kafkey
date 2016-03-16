# -*- coding:utf-8 -*-
from flask import json

__author__ = 'ylq'


class JsonResult(object):
    def __init__(self, total, rows):
        self.total = total
        self.rows = rows

    def __repr__(self):
        return json.dumps({'total': self.total, 'rows': self.rows})
