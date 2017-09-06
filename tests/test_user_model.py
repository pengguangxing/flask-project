# -*- coding: utf-8 -*-
import time
import unittest
from app.models import User
from app import db


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        """测试密码设置"""
        u = User(password='cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_no_getter(self):
        """验证密码没有getter属性"""
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        """验证密码校验"""
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salt_random(self):
        """验证加盐随机"""
        u = User(password='cat')
        u2 = User(password='cat')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        """有效确认令牌生成与确认"""
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(token is not None)
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        """验证不同用户的令牌不能相互确认"""
        u1 = User(password='cat')
        u2 = User(password='cat')
        db.session.add_all([u1, u2])
        db.session.commit()
        token = u1.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))

    def test_expired_confirmation_token(self):
        """验证令牌超时期限"""
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(expiration=2)
        time.sleep(4)
        self.assertFalse(u.confirm(token))

    def test_valid_reset_token(self):
        """验证正常重置密码"""
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_reset_token()
        self.assertTrue(u.reset_password(token, 'dog'))
        self.assertTrue(u.verify_password('dog'))

    def test_invalid_reset_token(self):
        """验证用户使用别的用户token不能重置密码"""
        u1 = User(password='cat')
        u2 = User(password='dog')
        db.session.add_all([u1, u2])
        db.session.commit()
        token = u1.generate_reset_token()
        self.assertFalse(u2.reset_password(token, 'jack'))
        self.assertTrue(u2.verify_password('dog'))


