# -*- coding: utf-8 -*-
import time
import unittest
from datetime import datetime
from app.models import User, Role, Permission, AnonymousUser, Follow
from app import db, create_app


class UserModelTestCase(unittest.TestCase):
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

    def test_role_and_permissions(self):
        """验证管理员和普通用户权限"""
        Role.insert_roles()
        u1 = User(email='pengguangxing1990@163.com', password='cat')
        u2 = User(email='john@qq.com', password='cat')
        self.assertTrue(u1.is_administrator())
        self.assertTrue(u1.can(Permission.FOLLOW))
        self.assertTrue(u2.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u2.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        """验证匿名用户不具权限"""
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))

    def test_ping(self):
        """验证刷新最后访问时间的方法"""
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        time.sleep(2)
        last_seen_before = u.last_seen
        u.ping()
        self.assertTrue(u.last_seen > last_seen_before)


    def test_follows(self):
        u1 = User(email='123@qq.com', password='cat')
        u2 = User(email='456@qq.com', password='dog')
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertFalse(u1.is_followed_by(u2))
        u1.follow(u2)
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertTrue(u2.is_followed_by(u1))
        self.assertFalse(u1.is_followed_by(u2))
        self.assertTrue(u1.followed.count() == 2)
        self.assertTrue(u2.followers.count() == 2)
        u1.unfollow(u2)
        db.session.add(u1)
        db.session.commit()
        self.assertTrue(u1.followed.count() == 1)
        self.assertTrue(u2.followers.count() == 1)
        self.assertTrue(Follow.query.count() == 2)
        u2.follow(u1)
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        db.session.delete(u2)
        db.session.commit()
        self.assertTrue(Follow.query.count() == 1)

    def test_to_json(self):
        u = User(email='john@example.com', password='cat')
        db.session.add(u)
        db.session.commit()
        json_user = u.to_json()
        expected_keys = ['url', 'username', 'member_since', 'last_seen',
                         'posts', 'followed_posts', 'post_count']
        self.assertEqual(sorted(json_user.keys()), sorted(expected_keys))
        self.assertTrue('api/v1.0/users/' in json_user['url'])
