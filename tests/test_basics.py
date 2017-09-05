# -*- coding: utf-8 -*-
import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        """搭建测试环境"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        """还原测试环境"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        """验证实例创建成功"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """验证实例处于测试模式"""
        self.assertTrue(current_app.config['TESTING'])



