from flask import Blueprint

auth = Blueprint('auth', __name__)
'''
Blueprint至少两个参数：蓝图名字，蓝图所在的包或模块
将这部分独立出来
'''

from . import views
