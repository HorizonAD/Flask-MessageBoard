from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import Required, Length, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(1, 64)])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[
        Required(), Length(1, 64)])
    password = PasswordField('密码(至少五位)', validators=[
        Required(),Length(min=5, max=25), EqualTo('password2', message='两次输入密码必须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    location = StringField('所在地(选填)')
    about_me = TextAreaField('关于我(选填)')
    submit = SubmitField('注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), Length(min=5, max=25), EqualTo('password2', message='两次输入密码必须一致')])
    password2 = PasswordField('确认新密码', validators=[Required()])
    submit = SubmitField('修改密码')