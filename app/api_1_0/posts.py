# -*- coding: utf-8 -*-
from flask import url_for, request, jsonify, g
from . import api
from .decorators import permission_required
from .. import db
from ..models import Post, Permission
from .errors import forbidden


@api.route('/posts/')
def get_posts():
    """获取所有文章的方法"""
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, 25, error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    """"获取一篇文章的api, 默认方法GET"""
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    """发布新文章的api.方法使POST,返回json数据、成功状态、和Location首部字段"""
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
           {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('权限不足')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())


