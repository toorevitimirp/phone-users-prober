from flask import Blueprint

predict = Blueprint('predict', __name__, url_prefix='/train/api/v1.0')

from predict import sgd_pred
