#coding=utf8
from flask import Flask, request
from flaskext.babel import Babel

app = Flask(__name__)
app.config.from_object('wiki.config')
app.config.from_envvar('WIKI_SETTINGS', silent=True)

babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['it', 'en'])

import wiki.views
