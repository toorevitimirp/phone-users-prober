from flask import Blueprint

train = Blueprint('train', __name__, url_prefix='/train/api/v1.0')

from train import train_submit
