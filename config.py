import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

# 初始化配置


class Config:
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)  # 会话过期时间
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you cannot guess me'
    WTF_CSRF_SECRET_KEY = 'this is very difficult'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_USERS_PER_PAGE = 10
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    # 上传图片配置
    UPLOAD_FOLDER = os.getcwd()+'/app/upload/avatar'
    THUMBNAIL_FOLDER = os.getcwd()+'/app/upload/avatar-thumbnail'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 文件最大限制16M,仅需配置
    ALLOWED_EXTENSIONS = set(['bmp', 'svg', 'png', 'jpg', 'jpeg', 'gif'])
    # 邮件配置
    FLASKQ_MAIL_SENDER = '吐槽'
    MAIL_SERVER = "smtp.163.com"
    MAIL_PROT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    # ennn..我知道密码上传了,这个邮箱测试用
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or "flywinky@163.com"
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or "lclxzhavyznfc163"
    MAIL_DEBUG = True
    # debugtoolbar配置
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True  # 性能显示
    DEBUG_TB_INTERCEPT_REDIRECTS = False  # 不拦截重定向
    # flask-babelex配置,汉化admin页面
    BABEL_DEFAULT_LOCALE = 'zh_CN'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data/data-dev.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data/data.sqlite')


# 配置封装，可以对开发，测试，生成分开配置
config = {
    'development': DevelopmentConfig,
    'Production': ProductionConfig,
    'default': DevelopmentConfig
}
