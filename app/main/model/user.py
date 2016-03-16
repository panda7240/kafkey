# -*- coding:utf-8 -*-

import json
from app import db
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    mail = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    type = db.Column(db.Integer)
    state = db.Column(db.Integer)
    create_time = db.Column(db.String(30))
    update_time = db.Column(db.String(30))

    def to_dict(self):
        d = dict()
        d["id"] = self.id
        d["name"] = self.name
        d["mail"] = self.mail
        d["phone"] = self.phone
        d["type"] = self.type
        d["state"] = self.state
        d["create_time"] = self.create_time
        d["update_time"] = self.update_time
        return d

    def __repr__(self):
        return json.dumps(self.to_dict())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
