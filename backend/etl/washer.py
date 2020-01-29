import pandas as pd
from flask import jsonify, request,Blueprint
from flask_cors import cross_origin
from statistic.describe import describe
from etl.database import save_file

washer = Blueprint('washer', __name__,url_prefix='/wash-data')

def z_score(clean_data):
    #z-score规范化
    pass


def max_min(clean_data):
    #max-min规范化
    pass

def wash_data(user_data):
    #剔除含有非数值型数据的行
    user_data.dropna(inplace=True)
    for column in user_data.columns:
        if user_data[column].dtype=="object":
            del_list = []
            i = 0
            for val in user_data[column]:
                if not str(val).isdigit():
                    del_list.append(i)
                i += 1
            user_data.drop(del_list,inplace=True)
    return user_data


@washer.route('/api/v1.0/data',methods=['POST'])
@cross_origin()
def get_data_from_request():
    if request.method == 'POST':
        user_data = pd.read_csv(request.files["data_all"],encoding='utf-8')
        complain_users = pd.read_csv(request.files["data_label"],encoding='utf-8')["user_id"]
        collection = request.values['collection']
        all_users_id = user_data["user_id"]
        labels = all_users_id.isin(complain_users).astype("int")

        user_data["label"] = labels
        res = save_file(collection,user_data.to_json(orient='records'))
        return res
        # save_file(collection,user_data)
        
        # clean_data = wash_data(user_data)
        
        # descriptions = describe(clean_data)
        # return jsonify(descriptions)
