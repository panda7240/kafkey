# -*- coding:utf-8 -*-

from app import db
from app.main.model import BaseModel
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Message(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    mail = db.Column(db.String(128))
    phone = db.Column(db.String(128))
    type = db.Column(db.Integer)
    state = db.Column(db.Integer)
    create_time = db.Column(db.String(30))
    update_time = db.Column(db.String(30))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

