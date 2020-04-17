"""
对features按数据类型分类
"""
import common

import pandas as pd

from data_processing.data_utils import get_clean_raw_data

num_features = ['roam_call_duration', 'roam_duration_02', 'mon_use_days',
                'is_p_app_wx_times', 'zhujiao_time', 'zhujiao_times',
                'mb5', 'mb10', 'mb30', 'mb60', 'ma60', 'total_count',
                'beijiao_times', 'use_days', 'zhujiao', 'beijiao',
                'zhujiao_jt', 'open', 'close', 'open_day', 'cell_num']


def bool_num():
    # 测试feature的数据类型，(bool or numerical)
    bool_features = []
    num_features = []
    data = get_clean_raw_data()
    data = data.drop('label', 1)
    data = data.drop('user_id', 1)
    data = data.drop('_id', 1)
    for col in data.columns:
        zero_one = 0
        unique = data[col].unique()
        for k in [0, 1, '0', '1']:
            if k in unique:
                zero_one += data.groupby([col]).size()[k]

        all_count = data[col].count()

        if all_count == zero_one:
            bool_features.append(col)
        else:
            num_features.append(col)
    print(bool_features, num_features)


def disc_continuous():
    features = '../../data/3月用户相关数据.csv'
    label = '../../data/3月被投诉用户.csv'
    data = get_clean_raw_data(features_file=features, label_file=label)
    # data = get_clean_raw_data(features_file, label_file)
    for col in num_features:
        print(col)
        print(data[col].unique())


if __name__ == '__main__':
    disc_continuous()
