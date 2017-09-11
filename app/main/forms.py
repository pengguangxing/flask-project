# -*- coding: utf-8 -*-
from flask import current_app
from flask_wtf import FlaskForm
from flask_pagedown.fields import PageDownField
from wtforms import StringField, SubmitField, TextAreaField, BooleanField,SelectField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email
from ..models import Role, User


class PostForm(FlaskForm):
    body = PageDownField('发表您的文章', validators=[DataRequired()])
    submit = SubmitField('发表')


class EditProfileForm(FlaskForm):
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('提交')


class EditProfileAdminForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(),
                                          Length(1, 64), Email()])
    username = StringField('昵称', validators=[DataRequired(), Length(1, 64)])
    confirmed = BooleanField('确认')
    role = SelectField('角色', coerce=int)
    name = StringField('姓名', validators=[Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('自我介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        """role是SelectField的实例，其属性choices设置下拉选项。选项必须是由元组组成的列表，
        各元组包含2个元素：标识符和显示在控件的文本字符串（即role.id和role.name）。元组中标
        识符是角色id，是个整数，所以SelectField构造函数中coerce=int,从而把默认为字符串的字
        段值转换为整数。"""
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被别人使用')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('昵称已被别人使用')

    def validate_role(self, field):
        if self.user.email == current_app.config['FLASK_ADMIN'] and \
                        Role.query.get(field.data) != self.user.role:
            raise ValidationError('不允许修改超级管理员的角色权限')


class CommentForm(FlaskForm):
    body = StringField('', validators=[DataRequired()])
    submit = SubmitField('评论')

