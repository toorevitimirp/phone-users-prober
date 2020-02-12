from statistic import statistic
from flask import request
from flask_cors import cross_origin

@statistic.route('/basic', methods=['POST'])
@cross_origin()
def basic():
    pass