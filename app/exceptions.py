from flask_moment import Moment
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_pagedown import PageDown
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension
from flask_admin import Admin
from flask_babelex import Babel

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
csrf = CSRFProtect()
mail = Mail()
debugtoolbar=DebugToolbarExtension()
admin=Admin(name=u'后台')
babel=Babel()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

admin_login_manager = LoginManager()
admin_login_manager.session_protection = 'strong'
admin_login_manager.login_view = 'Admin.login'

class ValidationError(ValueError):
    pass
