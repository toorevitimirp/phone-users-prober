import json

from statistic import statistic
from flask import request
from flask_cors import cross_origin
from etl.data_utils import load_data
from statistic.util import process_bool_feature, process_num_feature


@statistic.route('/basic-num', methods=['POST'])
@cross_origin()
def basic_num():
    if request.method == 'POST':
        req_data = request.get_data()
        json_data = json.loads(req_data.decode('utf-8'))
        collection = json_data['collection']
        print(collection)

        raw = load_data(collection)
        num = process_num_feature(raw)
        # print(num)
        return {'result': 0, 'data': num}


@statistic.route('/basic-bool', methods=['POST'])
@cross_origin()
def basic_bool():
    if request.method == 'POST':
        req_data = request.get_data()
        json_data = json.loads(req_data.decode('utf-8'))
        collection = json_data['collection']

        raw = load_data(collection)

        data = process_bool_feature(raw)
        return {'result': 0, 'data': data}
