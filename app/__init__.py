# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from config import config


bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()
moment = Moment()


def create_app(config_name):
    """
    工厂函数创建程序实例，配置名对应的配置类，初始化扩展库, 注册蓝本。
    :param config_name: 配置名，来自配置文件注册的字典
    :return: app程序实例
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
