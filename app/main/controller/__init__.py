# -*- coding:utf-8 -*-
from functools import wraps
from flask import session, render_template


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print session.get('user')
        if session.get('user') is None:
            return render_template('login.html')
        return f(*args, **kwargs)
    return decorated_function

