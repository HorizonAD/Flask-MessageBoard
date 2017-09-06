import os.path as op
from flask import Flask
from config import config
from .admin import UserModelView,PostModelView,CommentModelView,FileAdmin
from flask_admin import AdminIndexView
from .exceptions import (
    bootstrap,
    moment,
    db,
    pagedown,
    csrf,
    mail,
    debugtoolbar,
    admin,
    login_manager,
    babel
)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    debugtoolbar.init_app(app)
    babel.init_app(app)
    admin.init_app(app,
        index_view=AdminIndexView(
            name=u'后台管理',
            template='admin/admin-v1.html',
            url='/6oPT' #这里可以自己生成很长的随机数
            )
        )
    admin.add_view(UserModelView(db.session,name='用户管理'))
    admin.add_view(PostModelView(db.session,name='留言管理'))
    admin.add_view(CommentModelView(db.session,name='评论管理'))
    #文件管理    
    path = op.join(op.dirname(__file__), 'upload/avatar')
    admin.add_view(FileAdmin(path, '/upload', name='文件管理'))    

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .Admin import admin as Admin_blueprint
    app.register_blueprint(Admin_blueprint, url_prefix='/admin') #这个url可以设置成随机种子以防爆破

    return app