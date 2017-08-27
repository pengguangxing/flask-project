# -*- coding: utf-8 -*-
# flask基础学习

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello,Test</h1>'


if __name__ == '__main__':
    app.run(debug=True)
