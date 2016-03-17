# -*- coding:utf-8 -*-
from app.main.controller import login_required, json_result
from app.main.model.user import User
from flask import render_template, session, redirect, url_for, current_app, request, Blueprint

user_blueprint = Blueprint('user_blueprint', __name__)


