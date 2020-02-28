import pandas as pd
import json
from flask import Blueprint, request
from flask_cors import cross_origin
from etl.data_utils import save_data, get_collection_info, del_data_by_collection_name, get_complained_users
from etl.washer import wash_data
from config import data_info, model_info
# from bson import json_util

data_center = Blueprint('data_center', __name__, url_prefix='/data-center/api/v1.0')


@data_center.route('/data', methods=['POST'])
@cross_origin()
def post_data():
    if request.method == 'POST':
        collection = request.values['collection']

        if collection == data_info or collection == model_info:
            return {'result': 500, 'msg': '上传失败，数据集合名称不符合规范'}

        # 将csv文件转换为标准的数据格式，保存features，label
        user_data = pd.read_csv(request.files["data_all"], encoding='utf-8')
        complain_users = pd.read_csv(request.files["data_label"], encoding='utf-8')["user_id"]
        all_users_id = user_data["user_id"]
        labels = all_users_id.isin(complain_users).astype("int")
        user_data["label"] = labels

        # 清洗数据
        clean_data = wash_data(user_data)

        # 数据持久化
        try:
            # 使用mongodb
            # length = clean_data.shape[0]
            # columns = list(clean_data.columns)
            # res = save_data(collection, clean_data.to_json(orient='records'), columns, length)

            # 保存为csv文件
            res = save_data(collection, clean_data)
        except BaseException as e:
            print("exception", e)
            res = {'result': 500, 'msg': '上传失败，未知错误'}
        finally:
            return res


@data_center.route('/data/info')
@cross_origin()
def get_data_info():
    try:
        collection_info = get_collection_info()
        res = {'result': 0, 'data': collection_info}
    except BaseException as e:
        print('exception:', e)
        res = {'result': 500, 'data': None}
    finally:
        return res


@data_center.route('/data/del', methods=['POST'])
@cross_origin()
def del_data():
    if request.method == 'POST':
        data = request.get_data()
        json_data = json.loads(data.decode('utf-8'))
        name = json_data['name']
    return del_data_by_collection_name(name)


@data_center.route('/complained-users', methods=['POST'])
@cross_origin()
def complained_users():
    if request.method == 'POST':
        req_data = request.get_data()
        json_data = json.loads(req_data.decode('utf-8'))
        collection = json_data['collection']
        print(json_data)
        data = get_complained_users(collection)
        data = data.to_json(orient='records')
        res = {'result': 0, 'data': data}
    return res
