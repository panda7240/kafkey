# -*- coding:utf-8 -*-

__author__ = 'ylq'

import json
from app import db


class Cluster(db.Model):
    __tablename__ = 'cluster'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    broker = db.Column(db.String(256))
    zookeeper = db.Column(db.String(256))
    remark = db.Column(db.String(256))
    create_time = db.Column(db.String(30))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def __repr__(self):
        return json.dumps(self.to_dict())
