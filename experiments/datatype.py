# import pandas as pd
from data import get_all_data

bool_features = ['users_3w', 'twolow_users', 'roam_users02', 'roam_users01',
                 'vv_type', 'in16_roam_tag']
num_features = ['roam_call_duration', 'roam_duration_02', 'mon_use_days',
                'is_p_app_wx_times', 'zhujiao_time', 'zhujiao_times',
                'mb5', 'mb10', 'mb30', 'mb60', 'ma60', 'total_count',
                'beijiao_times', 'use_days', 'zhujiao', 'beijiao',
                'zhujiao_jt', 'open', 'close', 'open_day', 'cell_num']


def bool_num():
    # 测试feature的数据类型，(bool or numerical)
    bool_features = []
    num_features = []
    data = get_all_data()
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


if __name__ == '__main__':
    bool_num()
