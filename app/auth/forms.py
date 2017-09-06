# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登入')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    username = StringField('昵称', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired(),
                                               EqualTo('password2', message='前后密码必须一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已经注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('昵称已经占用')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('原密码', validators=[DataRequired()])
    new_password = PasswordField('新密码', validators=[
        DataRequired(), EqualTo('new_password2', message='前后密码必须一致')])
    new_password2 = PasswordField('确认新密码', validators=[DataRequired()])
    submit = SubmitField('修改密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('注册邮箱', validators=[DataRequired(), Length(1, 64),
                                            Email()])
    submit = SubmitField('提交')


class PasswordResetForm(FlaskForm):
    email = StringField('邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField('新密码', validators=[DataRequired(),
                                               EqualTo('password2', message='前后密码必须一致')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('重置')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未知邮箱')




