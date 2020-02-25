import json

from statistic import statistic
from flask import request
from flask_cors import cross_origin
from etl.data_utils import get_complained_users
from statistic.util import process_bool_feature, process_num_feature


@statistic.route('/complained-num', methods=['POST'])
@cross_origin()
def complained_num():
    if request.method == 'POST':
        req_data = request.get_data()
        json_data = json.loads(req_data.decode('utf-8'))
        collection = json_data['collection']
        print(collection)

        raw = get_complained_users(collection)
        data = process_num_feature(raw)
        # print(num)
        return {'result': 0, 'data': data}


@statistic.route('/complained-bool', methods=['POST'])
@cross_origin()
def complained_bool():
    if request.method == 'POST':
        req_data = request.get_data()
        json_data = json.loads(req_data.decode('utf-8'))
        collection = json_data['collection']
        print(collection)

        raw = get_complained_users(collection)
        data = process_bool_feature(raw)
        # print(num)
        return {'result': 0, 'data': data}
