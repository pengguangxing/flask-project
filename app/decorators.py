# -*- coding: utf-8 -*-
"""自定义装饰器，让视图函数只对有特定权限的用户开放。
   可以像如下这么使用：
   @app.route('/')
   @permission_required(Permission.COMMENT)
   def index():
       return '<h1>Hello</h1>'
"""

from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)
