# -*- coding:utf-8 -*-
from functools import wraps
from flask import session, render_template
import json


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print session.get('user')
        if session.get('user') is None:
            return render_template('login.html')
        return f(*args, **kwargs)

    return decorated_function


# 将查询结果转化成json字符串,返回给前台页面
def json_result(total, rows):
    if total == 0:
        return json.dumps({'total': 0, 'rows': ''})
    if isinstance(rows[0], dict):
        return json.dumps({'total': total, 'rows': rows})
    else:
        return json.dumps({'total': total, 'rows': [r.to_dict() for r in rows]})
