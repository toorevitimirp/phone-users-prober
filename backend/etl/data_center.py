import pandas as pd
from flask import Blueprint,request
from flask_cors import cross_origin
from etl.database import save_file,get_collection_info
from etl.washer import wash_data

data_center = Blueprint('data_center', __name__,url_prefix='/data-center/api/v1.0')

@data_center.route('/data',methods=['POST'])
@cross_origin()
def post_data():
    if request.method == 'POST':
        collection = request.values['collection']
        if collection == 'data-info':
            return {'result':500,'msg':'上传失败，数据集合名称不能为data-info'}

        user_data = pd.read_csv(request.files["data_all"],encoding='utf-8')
        complain_users = pd.read_csv(request.files["data_label"],encoding='utf-8')["user_id"]
        all_users_id = user_data["user_id"]
        labels = all_users_id.isin(complain_users).astype("int")

        user_data["label"] = labels
        clean_data = wash_data(user_data)
        try:
            length = clean_data.shape[0]
            res = save_file(collection,clean_data.to_json(orient='records'),length)
        except BaseException as e:
            print("exception",e)
            res = {'result':500,'msg':'上传失败，未知错误'}
        finally:
            return res
        # save_file(collection,user_data)
        
        # clean_data = wash_data(user_data)
        
        # descriptions = describe(clean_data)
        # return jsonify(descriptions)

@data_center.route('/data/info')
@cross_origin()
def get_data_info():
    try:
        collection_info = get_collection_info()
        res = {'result':0,'data':collection_info}
    except BaseException as e:
        print('exception:',e)
        res = {'result':500,'data':None}
    finally:
        return res