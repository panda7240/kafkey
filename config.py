# -*- coding:utf-8 -*-
import logging

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # 是否开启message监控
    MESSAGE_MONITOR_OPEN = True
    LOG_LEVEL = 'INFO'
    LOG_FILE_PATH = 'kafkey.log'

    # 创建一个root logger
    logger = logging.getLogger('')
    # 创建一个handler，用于写入日志文件
    file_handler = logging.FileHandler(LOG_FILE_PATH)
    # 再创建一个handler，用于输出到控制台
    console_handler = logging.StreamHandler()
    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    estracer = logging.getLogger('elasticsearch.trace')
    estracer.setLevel(logging.INFO)
    estracer.addHandler(logging.FileHandler('es_trace.log'))

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    Config.logger.setLevel(logging.DEBUG)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

    Config.logger.setLevel(logging.DEBUG)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    Config.logger.setLevel(logging.INFO)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}


