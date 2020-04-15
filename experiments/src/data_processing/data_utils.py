"""
data_processing的主模块
"""
from collections import Counter

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
    user_data = pd.read_csv(features_file, encoding='utf-8', low_memory=False)
    complain_users = pd.read_csv(label_file, encoding='utf-8')["user_id"]

    all_users_id = user_data["user_id"]
    labels = all_users_id.isin(complain_users).astype("int")
    user_data["label"] = labels

    clean_data = _wash_data(user_data)
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


# def get_complained_users_id_real(features_file=None, label_file=None):
#     clean_data = get_clean_raw_data(features_file=features_file, label_file=label_file)
#     grouped = clean_data.groupby('label')
#     group_1 = grouped.get_group(1)
#     complained_users_id_real = group_1['user_id']
#     return np.array(complained_users_id_real)


def _delete_outliers(user_data):
    """
    删除outliers
    :param data: pandas.DataFrame
    :return: pandas.DataFrame
    """
    outlier_count = 0

    outlier_rules = {
                    'open': 100,
                    'close': 100,
                    'beijiao': 100,
                    'beijiao_times': 100,
                    'cell_num': 3000,
                    'zhujiao_jt': 10000,
                    'zhujiao': 7500,
                    'ma60': 800,
                    'mb5': 500,
                    'mb10': 1500,
                    'mb30': 2500,
                    'mb60': 600,
                    'total_count': 5000,
                    'zhujiao_time': 400000,
                    'zhujiao_times': 4000,
                    'roam_call_duration': 20000,
                    'roam_duration_02': 200000,
                    'is_p_app_wx_times': 20000
                    }
    for column in num_features:
        # user_data[np.abs(user_data[column] - user_data[column].mean()) <= (3 * user_data[column].std())]

        # threshold = 0.9
        # line = user_data[column].quantile(threshold)
        # median = user_data[column].describe()["50%"]
        #
        # user_data[column] = user_data[(user_data[column] < line)][column]
        #
        # count = user_data[column].isnull().sum()
        # outlier_count += count
        if column in outlier_rules.keys():
            threshold = outlier_rules[column]
            user_data[column] = user_data[(user_data[column] < threshold)][column]
            median = user_data[column].describe()["50%"]
            count = user_data[column].isnull().sum()
            outlier_count += count
            user_data[column].fillna(median, inplace=True)
        else:
            print(column)
    print('去掉的离群点个数：{}'.format(outlier_count))

    # y = user_data['label']
    # print('数值筛选前：', Counter(y))
    # # print(user_data)
    # # 如果这些特征数值较大，则为正常用户
    # select_rules = {'open': 100,
    #                 'close': 100,
    #                 'beijiao': 100,
    #                 'beijiao_times': 3000,
    #                 'cell_num': 8000,
    #                 'zhujiao_jt': 10000,
    #                 'zhujiao': 10000,
    #                 'ma60': 800,
    #                 'mb5': 500,
    #                 'mb10': 1500,
    #                 'mb30': 2500,
    #                 'mb60': 600,
    #                 'total_count': 5000,
    #                 'zhujiao_time': 400000,
    #                 'zhujiao_times': 4000,
    #                 'roam_call_duration': 20000,
    #                 'roam_duration_02': 200000,
    #                 'is_p_app_wx_times': 20000
    #                 }
    # # user_data['sel'] = 0
    # del_index = []
    # # indies = user_data.index
    # # print(user_data.iloc[172446])
    # # user_data.drop(172446, inplace=True)
    # # user_data.drop(172445, inplace=True)
    # # user_data.drop(172447, inplace=True)
    # wtf = 0
    # for column in select_rules.keys():
    #     i = 0
    #     for element in user_data[column]:
    #         if column == 'is_p_app_wx_times':
    #             print(select_rules[column])
    #             # print(user_data.iloc[i])
    #             # user_data.drop(index = i, inplace=True, axis=0)
    #         if element > select_rules[column]:
    #             del_index.append(i)
    #             wtf += 1
    #             # user_data['sel'][i] = 1
    #         i += 1
    # user_data = user_data.drop(labels=del_index, axis=0)
    #
    # print(user_data.shape)
    # print(len(del_index))
    # print(wtf)

    # user_data = user_data.groupby('sel').get_group(1)
    # fuck = 0
    # for i, element in enumerate(user_data['is_p_app_wx_times']):
    #     if element > 2500000:
    #         fuck += 1
    #         print(i)
    #         print(user_data.iloc[i])
    #         print('fuck', element)
    #         user_data.drop(i-1, inplace=True)
    # print(fuck)

    return user_data


def _wash_data(user_data):
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
                    print("删除列{},第{}行数据：{}".format(column, i, val))
                    del_list.append(i)
                i += 1
    user_data.drop(del_list, inplace=True)

    # delete outlier
    # print(user_data.describe())
    user_data = _delete_outliers(user_data)
    # data = _delete_outliers(data)
    # print(user_data.shape)
    return user_data


def prepare_data_4_training(features_file=None, label_file=None):
    """
    imbalanced data processing,降维，feature scaling，升维，获得模型训练能够直接用的数据
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

    # users_id = raw_data['user_id']

    return X_final, y


def prepare_data_4_prediction(features_file=None, label_file=None):
    """
    降维，feature scaling，升维，获得模型能够直接用的数据
    预测不需要处理imbalanced data，所以要和prepare_data_4_training分开
    :param features_file:
    :param label_file:
    :return:
    """
    raw_data = get_clean_raw_data(features_file=features_file,
                                  label_file=label_file)
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])
    print('特征集文件={},标签文件={}'.format(features_file, label_file))
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

    users_id = np.array(raw_data['user_id'])

    return X_final, y, users_id
