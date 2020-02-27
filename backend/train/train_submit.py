import json
from flask import request
from flask_cors import cross_origin
from concurrent.futures import ThreadPoolExecutor

from etl.database import get_collection_info, get_train_info_by_model, get_train_info_by_model_collection, \
    is_trained_model_collection
from train import train
from train.models import sgd_classifier


@train.route('/info', methods=['POST'])
@cross_origin()
def train_info():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        model_name = json_data['model']

        # 所有数据集的信息
        data_info = get_collection_info()
        # 已经由某模型(名称为model_name)训练过的数据集的名字
        trained_collection = [datum['collection_name'] for datum in get_train_info_by_model(model_name)]

        for datum in data_info:
            name = datum['name']
            # 如果该数据集已经由该模型训练
            if name in trained_collection:
                trained_one = \
                    get_train_info_by_model_collection(model=model_name, collection=name)
                datum['cost_time'] = trained_one['cost_time']
                datum['date'] = trained_one['date']
            else:
                datum['cost_time'] = 0
                datum['date'] = 0
        # print(data_info)

        res = {'result': 0, 'data': data_info}
        return res


@train.route('/', methods=['POST'])
@cross_origin()
def train_submit():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        model_name = json_data['model']
        collection = json_data['collection']

        if model_name == 'sgd':
            trained = is_trained_model_collection(model_name=model_name,
                                                  collection=collection)
            if trained:
                res = {'result': 0, 'msg': '该数据集已训练！'}
            else:
                executor = ThreadPoolExecutor(1)
                executor.submit(sgd_classifier, collection)
                res = {'result': 1, 'msg': '正在训练，需要一定时间...'}
        else:
            res = {'result': 0, 'msg': '模型名错误'}

        return res

