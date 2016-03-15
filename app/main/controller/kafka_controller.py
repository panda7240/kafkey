from app.main import main
from app.main.controller import login_required
from flask import render_template, session, redirect, url_for, current_app, request


@main.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('cluster/index.html', username=session.get("user"))
