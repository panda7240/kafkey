#!/usr/bin/env python
from flask.ext.script import Manager
import os
from app import create_app

app = create_app(os.getenv('KAFKEY_CONFIG') or 'default')

manager = Manager(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
