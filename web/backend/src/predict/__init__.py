from flask import Blueprint

predict = Blueprint('predict', __name__, url_prefix='/predict/api/v1.0')

from predict import pred_submit
