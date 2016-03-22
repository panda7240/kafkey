# -*- coding:utf-8 -*-

from app import db
from app.main.model import BaseModel
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Message(BaseModel):
    pass
