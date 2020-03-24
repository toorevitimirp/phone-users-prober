# 日志
import logging
import os
from datetime import date
from logging.handlers import RotatingFileHandler

from api.app import app
from config import log_dir


def log(msg):
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    file_handler = RotatingFileHandler(log_dir + str(date.today()) + '.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info(msg)
