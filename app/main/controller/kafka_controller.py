# -*- coding:utf-8 -*-

from app.main.controller import login_required
from flask import render_template, session, redirect, url_for, current_app, request, Blueprint

kafka_blueprint = Blueprint('kafka_blueprint', __name__)






