from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField,BooleanField
from wtforms.validators import Required,DataRequired, ValidationError,Length,EqualTo
from app.models import Admin,Role


class LoginForm(FlaskForm):
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_account(self,field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在！")

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), Length(min=5, max=25), EqualTo('password2', message='两次输入密码必须一致')])
    password2 = PasswordField('确认新密码', validators=[Required()])
    submit = SubmitField('修改密码')

class RoleAddForm(FlaskForm):
    role =StringField('角色名称', validators=[Required()])
    submit = SubmitField('添加')

class AdminAddForm(FlaskForm):
    adminname = StringField('管理员昵称', validators=[Required()])
    password = PasswordField('管理员密码', validators=[
        Required(), Length(min=5, max=25), EqualTo('password2', message='两次输入密码必须一致')])
    password2 = PasswordField('确认管理员新密码', validators=[Required()])
    roletype= SelectField(u'选择所属角色')
    submit = SubmitField('添加')

    def __init__(self,*args,**kwargs):
        super(AdminAddForm,self).__init__(*args,**kwargs)
        self.roletype.choices= [('','---选择角色类型---')]+[(role.name,role.name) for role in Role.query.all()]