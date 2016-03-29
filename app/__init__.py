# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from elasticsearch import Elasticsearch

db = SQLAlchemy()
bootstrap = Bootstrap()
moment = Moment()

es = None


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)

    global es
    if es is None:
        es = Elasticsearch(config[config_name].ES_HOSTS,sniffer_timeout=60)

    from app.main.controller.auth_controller import auth_blueprint

    app.register_blueprint(auth_blueprint)

    from app.main.controller.user_controller import user_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/user')

    from app.main.controller.kafka_controller import kafka_blueprint

    app.register_blueprint(kafka_blueprint, url_prefix='/kafka')

    from app.main.controller.message_controller import message_blueprint

    app.register_blueprint(message_blueprint, url_prefix='/message')

    from app.main.controller.monitorlog_controller import monitorlog_blueprint

    app.register_blueprint(monitorlog_blueprint, url_prefix='/monitorlog')

    return app
