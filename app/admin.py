#coding=utf-8
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_wtf import Form
from .models import User,Post,Comment

class FileAdmin(FileAdmin):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "八一":
            return True
        return False
    form_base_class = Form #CSRF引入 
    can_upload = False
    can_rename = False
    can_mkdir = False
        
class UserModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "八一":
            return True
        return False
    can_create = False

    column_labels = {
        'id':u'序号',
        'username' : u'昵称',
        'avatar':u'头像',
        'location':u'所在地',
        'about_me':u'个人说明'
    }
    column_list = ('id','username','avatar','location','about_me')
    def __init__(self, session, **kwargs):
        super(UserModelView, self).__init__(User, session, **kwargs)

class PostModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "八一":
            return True
        return False
    can_create = False

    column_labels = {
        'id':u'序号',
        'body' : u'内容',
        'body_html':u'HTML内容',
        'timestamp':u'发布时间'
    }
    column_list = ('id','body','body_html','timestamp')
    def __init__(self, session, **kwargs):
        super(PostModelView, self).__init__(Post, session, **kwargs)

class CommentModelView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "八一":
            return True
        return False
    can_create = False

    column_labels = {
        'id':u'序号',
        'body' : u'内容',
        'body_html':u'HTML生成',
        'comment_type':u'类型',
        'reply_to':u'回复对象',
        'timestamp':u'发布时间'
    }
    column_list = ('id','body','body_html','comment_type','reply_to','timestamp')
    def __init__(self, session, **kwargs):
        super(CommentModelView, self).__init__(Comment, session, **kwargs)                