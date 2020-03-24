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
        trained_collection_name = request.values['collection']
        model_name = request.values['model']

        # 将csv文件转换为标准的数据格式，保护features
        user_data = pd.read_csv(request.files["data_all"], encoding='utf-8')
        # all_users_id = user_data["user_id"]

        # 清洗数据
        X_pred = wash_data(user_data)
        print(X_pred)
        print(trained_collection_name)
        print(model_name)

        if model_name == 'sgd':
            is_trained = is_trained_model_collection(model_name=model_name,
                                                     collection=trained_collection_name)
            if not is_trained:
                res = {'result': 0, 'msg': '该数据集未训练！'}
            else:
                complained_users = pred_complained_users(trained_collection_name, X_pred, model_name)
                complained_users_dict = complained_users.to_json(orient='records')
                res = {'result': 1, 'msg': '返回成功', 'data': complained_users_dict}
        else:
            res = {'result': 0, 'msg': '模型名错误'}

        return res
