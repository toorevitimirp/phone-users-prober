"""
data_processing的主模块，其他包直接从该模块导入函数
"""
import common
import re
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

from data_processing.dimension_reduction import features_extraction_3d
from data_processing.imbalance_handle import imbalanced_handle

bool_features = ['users_3w', 'twolow_users', 'roam_users02', 'roam_users01',
                 'vv_type', 'in16_roam_tag']
num_features = ['roam_call_duration', 'roam_duration_02', 'mon_use_days',
                'is_p_app_wx_times', 'zhujiao_time', 'zhujiao_times',
                'mb5', 'mb10', 'mb30', 'mb60', 'ma60', 'total_count',
                'beijiao_times', 'use_days', 'zhujiao', 'beijiao',
                'zhujiao_jt', 'open', 'close', 'open_day', 'cell_num']


def _is_number(num):
    """
    使用正则表达式判断num是否为数字
    :param num:
    :return:
    """
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(str(num))
    if result:
        return True
    else:
        return False


def get_clean_raw_data(features_file=None, label_file=None):
    """
    返回清洗过的数据，没有其他处理
    :param features_file:
    :param label_file:
    :return:
    """
    user_data = pd.read_csv(features_file, encoding='utf-8')
    complain_users = pd.read_csv(label_file, encoding='utf-8')["user_id"]

    all_users_id = user_data["user_id"]
    labels = all_users_id.isin(complain_users).astype("int")
    user_data["label"] = labels

    clean_data = wash_data(user_data)
    # count1 = 0
    # for i, val in enumerate(clean_data['label']):
    #     if val == 1:
    #         print('1:', i, clean_data['user_id'][i])
    #         count1 += 1
    #     elif val == 0:
    #         pass
    #         # print('0:', clean_data['user_id'][i])
    #     else:
    #         print(val)
    #
    # print(count1)
    # print(clean_data.groupby('label')['twolow_users'].value_counts())
    return clean_data


def wash_data(user_data):
    user_data.dropna(inplace=True)

    replace_rule = {'0': 0, '1': 1, '公众': 0, '湖南长沙': 1}
    user_data.replace(replace_rule, inplace=True)
    # del_series=user_data.applymap(_is_number).all(1)
    # del_list = [i for i, x in enumerate(del_series) if x == False]
    # user_data.drop(del_list,inplace=True)

    # 剔除含有非数值型数据的行
    del_list = []
    for column in user_data.columns:
        if user_data[column].dtype == "object":
            i = 0
            for val in user_data[column]:
                if not str(val).replace(".", "").isdigit():
                    print("删除列{},第{}行数据：{}".format(column, i,val))
                    del_list.append(i)
                i += 1
    user_data.drop(del_list, inplace=True)
    return user_data


def prepare_data_4_model(features_file=None, label_file=None):
    """
    imbalanced data processing,降维，feature scaling，升维，获得模型能够直接用的数据
    注意处理顺序
    :param features_file:
    :param label_file:
    :return:
    """
    raw_data = get_clean_raw_data(features_file=features_file,
                                  label_file=label_file)
    # all_features = num_features + bool_features
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])
    print('特征集文件={},标签文件={}'.format(features_file, label_file))
    print('原始特征维度：', X.shape[1])

    # imbalanced data processing
    X_sample, y = imbalanced_handle(X, y)

    # 降维
    X_extract = features_extraction_3d(X_sample)
    # print(X_extract)

    # feature scaling -> 升维 -> feature scaling
    X_scaled = preprocessing.scale(X_extract)
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X_scaled)
    X_scaled_poly = preprocessing.scale(X_poly)

    X_final = X_scaled_poly
    print('训练的特征维度：', X_final.shape[1])

    users_id = raw_data['user_id']

    return X_final, y, users_id

