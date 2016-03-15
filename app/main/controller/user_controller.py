from app.main import main
from app.main.controller import login_required
from flask import render_template, session, redirect, url_for, current_app, request


@main.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html', username=session.get("user"))


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method != 'POST':
        from jinja2 import TemplateNotFound

        try:
            return render_template('login.html')
        except TemplateNotFound:
            from os import abort

            abort(404)
    userName = request.values.get('user_account')
    password = request.values.get('user_pwd')
    if userName == 'admin' and password == 'test':
        session['user'] = userName
        return 'SUCCESS'
    else:
        pass


@main.route('/logout')
def logout():
    session['user'] = None
    return redirect("/")
