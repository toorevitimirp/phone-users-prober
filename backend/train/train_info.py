import json
from flask import request
from flask_cors import cross_origin

from etl.database import get_collection_info, get_train_info_by_model, get_train_info_by_model_collection
from train import train


@train.route('/all-collection-model', methods=['POST'])
@cross_origin()
def get_trained_collection():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        model_name = json_data['model']

        # 已经由某模型(名称为model_name)训练过的数据集的名字
        trained_collection = [datum['collection_name'] for datum in get_train_info_by_model(model_name)]
        data = [{'name': name} for name in trained_collection]
        return {'result': 0, 'data': data}


@train.route('/info', methods=['POST'])
@cross_origin()
def train_all_info():
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
                datum['precision'] = trained_one['precision']
                datum['recall'] = trained_one['recall'],
                datum['f1_score'] = trained_one['f1_score']
            else:
                datum['cost_time'] = -1
                datum['date'] = -1
                datum['precision'] = -1
                datum['recall'] = -1
                datum['f1_score'] = -1
        # print(data_info)

        res = {'result': 0, 'data': data_info}
        return res
