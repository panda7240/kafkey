#!/usr/bin/env python
import time
from app import create_app, db
from app.main.model.user import User
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('KAFKEY_CONFIG') or 'default')
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
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)





if __name__ == '__main__':
    manager.run()

