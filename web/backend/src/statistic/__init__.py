from flask import Blueprint

statistic = Blueprint('statistic', __name__, url_prefix='/statistic/api/v1.0')

from statistic import basic
from statistic import  complained
# 必须引入视图文件
