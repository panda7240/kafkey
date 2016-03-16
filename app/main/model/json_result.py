# -*- coding:utf-8 -*-
from flask import json

__author__ = 'ylq'


class JsonResult(object):
    def __init__(self, total, rows):
        self.total = total
        self.rows = [r.to_dict() for r in rows]

    def __repr__(self):
        return json.dumps(self.__dict__)
