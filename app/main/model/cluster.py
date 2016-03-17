# -*- coding:utf-8 -*-
from app.main.model import BaseModel

__author__ = 'ylq'

from app import db


class Cluster(db.Model, BaseModel):
    __tablename__ = 'cluster'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    broker = db.Column(db.String(256))
    zookeeper = db.Column(db.String(256))
    remark = db.Column(db.String(256))
    create_time = db.Column(db.String(30))
