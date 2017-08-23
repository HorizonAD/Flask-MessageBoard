from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField,SubmitField
from wtforms.validators import Required, Length
from flask_pagedown.fields import PageDownField
from wtforms import ValidationError
from ..models import User


class NameForm(FlaskForm):
    name = StringField('昵称', validators=[Required()])
    submit = SubmitField('提交')


class EditProfileForm(FlaskForm):
    name = StringField('昵称', validators=[Required(),Length(0, 64)])
    location = StringField('所在地', validators=[Length(0, 64)])
    about_me = TextAreaField('关于我')
    submit = SubmitField('提交')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')

class PostForm(FlaskForm):
    body = PageDownField("说点什么吧", validators=[Required()])
    submit = SubmitField('提交')

class CommentForm(FlaskForm):
    body = StringField("评论",validators=[Required()])
    submit = SubmitField('提交')

class UploadForm(FlaskForm):
    image = FileField(u'选择文件', validators=[Required()])
    submit = SubmitField('提交')