from flask import jsonify
from api.app import app
from flask_cors import cross_origin


@app.errorhandler(404)
@cross_origin()
def not_found_error(error):
    return jsonify({'result': 404, 'msg': 'resource not found'})


@app.errorhandler(500)
@cross_origin()
def internal_error(error):
    return jsonify({'result': 500, 'msg': 'unknow error'})
