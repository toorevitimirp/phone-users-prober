import json
import pandas as pd
from flask import request
from flask_cors import cross_origin
from concurrent.futures import ThreadPoolExecutor

from etl.database import is_trained_model_collection
from etl.washer import wash_data
from predict import predict
from predict.models import pred_complained_users


@predict.route('/', methods=['POST', 'GET'])
@cross_origin()
def pred_submit():
    if request.method == 'POST':
        collection_trained = request.values['collection']
        model = request.values['model']

        # 将csv文件转换为标准的数据格式，保护features
        user_data = pd.read_csv(request.files["data_all"], encoding='utf-8')
        all_users_id = user_data["user_id"]

        # 清洗数据
        clean_data = wash_data(user_data)
        print(clean_data)
        print(collection_trained)
        print(model)
        # data = request.get_data()
        # json_data = json.loads(data.decode('utf-8'))
        # model_name = json_data['model']
        # trained_col = json_data['trained']
        # pred = json_data['pred']
        #
        # if model_name == 'sgd':
        #     is_trained = is_trained_model_collection(model_name=model_name,
        #                                              collection=trained_col)
        #     if not is_trained:
        #         res = {'result': 0, 'msg': '该数据集未训练！'}
        #     else:
        #         data = pred_complained_users(trained_col, pred, model_name)
        #
        #         res = {'result': 1, 'msg': '返回成功', 'data': data}
        # else:
        #     res = {'result': 0, 'msg': '模型名错误'}
        #
        # return res
        data = [{'feature': 'fuck'}, {'feature': 'fuck'}]
        return {'result': 0, 'data': data}
