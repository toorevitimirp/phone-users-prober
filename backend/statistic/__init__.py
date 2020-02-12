from flask import Blueprint

statistic = Blueprint('statistic', __name__, url_prefix='/statistic/api/v1.0')

from visualization import boxplot  # 必须引入视图文件