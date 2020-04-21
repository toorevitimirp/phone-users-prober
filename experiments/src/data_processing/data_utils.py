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


def _remove_filers_with_boxplot(data):
    print('根据boxplot去掉异常值前：', format(data.shape))
    p = data.boxplot(return_type='dict')
    for index,value in enumerate(data.columns):
        # 获取异常值
        fliers_value_list = p['fliers'][index].get_ydata()
        # 删除异常值
        for flier in fliers_value_list:
            data = data[data.loc[:, value] != flier]

    print('根据boxplot去掉异常值后：', format(data.shape))
    return data


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


def _delete_outliers_by_lof(user_data):
    """
    :param user_data: pandas.DataFrame
    :return: pandas.DataFrame
    """
    from sklearn.neighbors import LocalOutlierFactor
    clf = LocalOutlierFactor()
    # columns = user_data.columns.values.tolist()
    X = user_data.values
    y_pred = clf.fit_predict(X)
    user_data['is_inlier'] = y_pred

    result = user_data.groupby('is_inlier').get_group(1)

    print('去掉离群点个数:{}'.format(sum(np.array(y_pred) == -1)))
    return result


def _delete_outliers_by_rule(user_data):
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

    return user_data


def _remove_filers_by_quantile(data):
    """

    :param data: pandas.DataFrame
    :return: pandas.DataFrame
    """
    y = data['label']
    outlier_rules = {
        'open': 50,
        'close': 70,
        'beijiao': 50,
        'beijiao_times': 4200,
        'cell_num': 300,
        'zhujiao_jt': 9000,
        'zhujiao': 8000,
        'ma60': 400,
        'mb5': 500,
        'mb10': 800,
        'mb30': 2500,
        'mb60': 800,
        'total_count': 5000,
        'zhujiao_time': 400000,
        'zhujiao_times': 4000,
        'roam_call_duration': 2000,
        'roam_duration_02': 200000,
        'is_p_app_wx_times': 15000,
    }
    for index, row in data.iteritems():
        if index in outlier_rules.keys():
            outlier_count = 0
            complained_outlier_count = 0
            # threshold = row.quantile(0.95)
            threshold = outlier_rules[index]
            mean = row.mean()
            median = row.median()
            for i, v in row.items():
                if v > threshold:
                    if y[i] == 1:
                        complained_outlier_count += 1
                    else:
                        outlier_count += 1
                        row[i] = median
            print(index, ' outliers:', outlier_count, ' complained:', complained_outlier_count)

    return data


def _delete_outliers(user_data):
    """
    删除outliers
    :param data: pandas.DataFrame
    :return: pandas.DataFrame
    """
    user_data = _remove_filers_by_quantile(user_data)
    # user_data = _delete_outliers_by_lof(user_data)
    return user_data


def _print_basic_info(data):
    tests = [0.8, 0.85, 0.9, 0.95, 1]
    print('\t\t', end='\t')
    for i in tests:
        print(i, end='\t')
    print('\n')
    for column in num_features:
        print(column, end='\t')
        for v in tests:
            print(data[column].quantile(v), end='\t')
        print('\n')


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

    user_data = _delete_outliers(user_data)

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


def _get_outliers_rules():

    features = '../../data/4月用户相关数据.csv'
    label = '../../data/4月被投诉用户.csv'

    user_data = pd.read_csv(features, encoding='utf-8', low_memory=False)
    complain_users = pd.read_csv(label, encoding='utf-8')["user_id"]

    all_users_id = user_data["user_id"]
    labels = all_users_id.isin(complain_users).astype("int")
    user_data["label"] = labels

    maxs = []
    complain_users = user_data.groupby('label').get_group(1)
    for index, row in complain_users.iteritems():
        if index in num_features:
            _max = row.max()
            # print(index, ':', _max)
            maxs.append(_max)

    # print('______________________\n')
    thresholds = []
    for index, row in user_data.iteritems():
        if index in num_features:
            threshold = row.quantile(0.95)
            # print(index, ':', threshold)
            thresholds.append(threshold)

    df = pd.DataFrame()
    df['column'] = pd.Series(num_features)
    df['max'] = pd.Series(maxs)
    df['threshold'] = pd.Series(thresholds)
    print(df)


if __name__ == '__main__':
    _get_outliers_rules()