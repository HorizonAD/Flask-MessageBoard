import os
basedir = os.path.abspath(os.path.dirname(__file__))

#初始化配置
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you cannot guess me'
    SSL_DISABLE = False #默认打开SSL
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME=0.5
    #上传图片配置
    UPLOAD_FOLDER= os.getcwd()+'/app/upload/avatar'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 #文件最大限制16M,仅需配置
    ALLOWED_EXTENSIONS = set(['bmp','svg','png','jpg','jpeg','gif'])

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

#配置封装，可以对开发，测试，生成分开配置
config={  
        'development':DevelopmentConfig,
        'Production':ProductionConfig, 
        'default':DevelopmentConfig  
} 