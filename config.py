# -*- coding: utf-8 -*-
import os


class BaseConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
                 '\x97\xdd#\x1d\x8a\xf1\x87\xd3\xc6\x021\x02\x03\x12M\xa4u,\xfb.>\x82\xe4K'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SUBJECT_PREFIX = '[PGX]'
    MAIL_SENDER = 'pengguangxing<pengguangxing@aliyun.com>'
    FLASK_ADMIN = 'pengguangxing1990@163.com'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:1234@localhost/flask'
    MAIL_SERVER = 'smtp.aliyun.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://admin:1234@localhost/flasktest'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
