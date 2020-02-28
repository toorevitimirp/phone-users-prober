"""
提供能够直接给模型训练的数据
"""
import re
import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import PolynomialFeatures

from etl.data_utils import load_data
from etl.dimension_reduction import features_extraction_3d
from etl.imbalance_handle import imbalanced_handle

bool_features = ['users_3w', 'twolow_users', 'roam_users02', 'roam_users01',
                 'vv_type', 'in16_roam_tag']
num_features = ['roam_call_duration', 'roam_duration_02', 'mon_use_days',
                'is_p_app_wx_times', 'zhujiao_time', 'zhujiao_times',
                'mb5', 'mb10', 'mb30', 'mb60', 'ma60', 'total_count',
                'beijiao_times', 'use_days', 'zhujiao', 'beijiao',
                'zhujiao_jt', 'open', 'close', 'open_day', 'cell_num']


def prepare_data_4_training(collection):
    """
    imbalanced data processing,降维，feature scaling，升维，获得模型训练能够直接用的数据
    注意处理顺序
    :param features_file:
    :param label_file:
    :return:
    """
    raw_data = load_data(collection)
    # all_features = num_features + bool_features
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])
    print('数据集={}'.format(collection))
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

    return X_final, y


# def prepare_data_4_prediction(collection):
#     """
#     降维，feature scaling，升维，获得模型能够直接用的数据
#     预测不需要处理imbalanced data，所以要和prepare_data_4_training分开
#     :param collection: 数据集名称
#     :return:
#     """
#     raw_data = load_data(collection)
#     X = np.array(raw_data[num_features])
#     y = np.array(raw_data['label'])
#     print('原始特征维度：', X.shape[1])
#
#     # 降维
#     X_extract = features_extraction_3d(X)
#
#     # feature scaling -> 升维 -> feature scaling
#     X_scaled = preprocessing.scale(X_extract)
#     poly = PolynomialFeatures(degree=3)
#     X_poly = poly.fit_transform(X_scaled)
#     X_scaled_poly = preprocessing.scale(X_poly)
#
#     X_final = X_scaled_poly
#     print('训练的特征维度：', X_final.shape[1])
#
#     users_id = np.array(raw_data['user_id'])
#
#     return X_final, y, users_id
def prepare_data_4_prediction(X_pred):
    """
    降维，feature scaling，升维，获得模型能够直接用的数据
    预测不需要处理imbalanced data，所以要和prepare_data_4_training分开
    :param X_pred: 待预测的数据集
    :return:np.ndarray
    """

    X = np.array(X_pred[num_features])
    print('原始特征维度：', X.shape[1])

    # 降维
    X_extract = features_extraction_3d(X)

    # feature scaling -> 升维 -> feature scaling
    X_scaled = preprocessing.scale(X_extract)
    poly = PolynomialFeatures(degree=3)
    X_poly = poly.fit_transform(X_scaled)
    X_scaled_poly = preprocessing.scale(X_poly)

    X_final = X_scaled_poly
    print('训练的特征维度：', X_final.shape[1])

    return X_final