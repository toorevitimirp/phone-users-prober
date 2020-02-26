from flask import Blueprint

visual = Blueprint('visual', __name__, url_prefix='/visual/api/v1.0')

from visualization import boxplot  # 必须引入视图文件
from visualization import scatterplot
from visualization import histplot
from visualization import pieplot
