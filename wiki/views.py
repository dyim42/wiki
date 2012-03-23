#coding=utf8

import re

from . import app
from .models import db_session, Page
from flaskext.babel import gettext as _
from flask import (
    Flask,
    Markup,
    request,
    session,
    g,
    redirect,
    url_for,
    abort,
    render_template,
    flash,
    json,
    Response,
    )

wikiwords = re.compile(r'\b([A-Z][a-z]+[A-Z][a-z]+)')

@app.route('/')
def view_wiki():
    return redirect(url_for('view_page', name='FrontPage'))

@app.route('/<name>')
def view_page(name):
    page = Page.query.get(name)
    if page is None:
        return redirect(url_for('edit_page', name=name))

    def check(match):
        word = match.group(1)
        if Page.query.get(word):
            url = url_for('view_page', name=word)
        else:
            url = url_for('edit_page', name=word)
        return Markup('<a href="%s">%s</a>') % (url, word)

    content = wikiwords.sub(check, Markup.escape(page.data))
    edit_url = url_for('edit_page', name=name)
    return render_template('view.html', page=page, content=content, edit_url=edit_url)

@app.route('/edit/<name>', methods=['GET', 'POST'])
def edit_page(name):
    page = Page.query.get(name) or Page(name,'')
    if request.method == 'POST':
        page.data = request.form['body']
        db_session.add(page)
        db_session.commit()
        return redirect(url_for('view_page', name=name))

    save_url = url_for('edit_page', name=name)
    return render_template('edit.html', page=page, save_url=save_url)
