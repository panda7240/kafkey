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
    state = db.Column(db.Integer)
    create_time = db.Column(db.String(30))
    update_time = db.Column(db.String(30))

    def to_dict(self):
        d = dict()
        d["id"] = self.id
        d["name"] = self.name
        d["broker"] = self.broker
        d["zookeeper"] = self.zookeeper
        d["remark"] = self.remark
        d["state"] = self.state
        d["create_time"] = self.create_time
        d["update_time"] = self.update_time
        return d

    def __repr__(self):
        return json.dumps(self.to_dict())
