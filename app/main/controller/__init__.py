# -*- coding:utf-8 -*-
from functools import wraps
from flask import session, render_template, request
import json


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
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



class PageObj(dict):
    pass


def case_from_request(Clazz=None, limit=False, ispage=False):
    '''
    生成Clazz对象, request里的参数会注入为该对象的属性
    '''
    if Clazz == None:
        o = PageObj()
    else:
        o = Clazz()
    _dict = []
    if limit:
        #如果要求生成的对象里不能包含类定义以外的参数
        _dict = [d for d in Clazz.__dict__ if not d.startswith('_')]

    for r in request.values:
        if (not limit) or (r in _dict):
            o.__setattr__(r, request.values.get(r))

    if ispage: #如果需要分页
        if 'page' not in o.__dict__:
            o.__setattr__('page', 1)
        if 'rows' not in o.__dict__:
            o.__setattr__('rows', 30)
        o.page = int(o.page)
        o.rows = int(o.rows)
        o.__setattr__('offset', (o.page - 1) * o.rows)
    return o