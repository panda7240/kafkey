#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
from app import create_app, db
from app.main.model.user import User
from config import config
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


COV = None
if os.environ.get('KAFKEY_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()


config_name = os.getenv('KAFKEY_CONFIG') or 'default'
app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

@manager.command
def initdb():
    """Create db tables and init data"""
    db.drop_all()
    db.create_all()
    user_admin = User(name='admin', password='test', type=1, state=1, create_time=time.strftime('%Y-%m-%d %X', time.localtime()))
    user_manager = User(name='manager', password='test', type=2, state=1, create_time=time.strftime('%Y-%m-%d %X', time.localtime()))
    user_guest = User(name='guest', password='test', type=3, state=1, create_time=time.strftime('%Y-%m-%d %X', time.localtime()))
    db.session.add(user_admin)
    db.session.add(user_manager)
    db.session.add(user_guest)


@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('KAFKEY_COVERAGE'):
        import sys
        os.environ['KAFKEY_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

@manager.command
def printconfig():
    print config[config_name].LOG_LEVEL



if __name__ == '__main__':
    manager.run()

