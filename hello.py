# -*- coding: utf-8 -*-
# flask基础学习

from flask import Flask, make_response,render_template
from flask_script import Manager


app = Flask(__name__)

manager = Manager(app)

app.config['debug'] = True


@app.route('/')
@app.route('/<username>')
def index(username=None):
    if username is None:
        name = 'World'
    else:
        name = username
    resp = make_response(render_template('index.html', name=name))
    resp.set_cookie('pengguangxing', '123456')
    return resp


if __name__ == '__main__':
    manager.run()
