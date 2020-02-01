import pandas as pd
import numpy as np
import re,api
from flask import jsonify, request,Blueprint
from flask_cors import cross_origin
from statistic.describe import describe
from etl.database import save_file,get_collection_names

from time import time
washer = Blueprint('washer', __name__,url_prefix='/wash-data')

def _z_score(clean_data):
    #z-score规范化
    pass


def _max_min(clean_data):
    #max-min规范化
    pass

def _is_number(num):
  pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
  result = pattern.match(str(num))
  if result:
    return True
  else:
    return False 
def wash_data(user_data):
    #剔除含有非数值型数据的行
    start = time()
    user_data.dropna(inplace=True)
    # del_series=user_data.applymap(_is_number).all(1)
    # del_list = [i for i, x in enumerate(del_series) if x == False]
    # user_data.drop(del_list,inplace=True)

    del_list=[]
    for column in user_data.columns:
        if user_data[column].dtype=="object":
            i = 0
            for val in user_data[column]:
                if not str(val).replace(".","").isdigit():
                    del_list.append(i)
                i += 1
    user_data.drop(del_list,inplace=True)
    end = time()
    api.logger.log("去掉的行数: "+str(len(del_list)))
    api.logger.log("清洗数据所用时间：" + str(end-start))
    return user_data


@washer.route('/api/v1.0/data',methods=['POST'])
@cross_origin()
def post_data():
    if request.method == 'POST':
        user_data = pd.read_csv(request.files["data_all"],encoding='utf-8')
        complain_users = pd.read_csv(request.files["data_label"],encoding='utf-8')["user_id"]
        collection = request.values['collection']
        all_users_id = user_data["user_id"]
        labels = all_users_id.isin(complain_users).astype("int")

        user_data["label"] = labels
        clean_data = wash_data(user_data)
        try:
            res = save_file(collection,clean_data.to_json(orient='records'))
        except:
            res = {'result':500,'msg':'上传失败，未知错误'}
        finally:
            return res
        # save_file(collection,user_data)
        
        # clean_data = wash_data(user_data)
        
        # descriptions = describe(clean_data)
        # return jsonify(descriptions)

@washer.route('/api/v1.0/data/',methods=['GET'])
@cross_origin()
def get_data_list():
    try:
        collection_names = get_collection_names()
        res = {'result':200,'data':collection_names}
    except BaseException as e:
        print('exception:',e)
        res = {'result':500,'data':None}
    finally:
       return res
# def get_data(collection):
#     try:
#         user_data = load_data(collection)
#         print(user_data)
#         res = {'result':200,'data':user_data.to_json()}
#     except BaseException as e:
#         print('exception:',e)
#         res = {'result':500,'data':None}
#     finally:
#        return res
