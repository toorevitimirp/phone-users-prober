import pandas as pd

from washer import wash_data

bool_features = ['users_3w', 'twolow_users', 'roam_users02', 'roam_users01',
                 'vv_type', 'in16_roam_tag']
num_features = ['roam_call_duration', 'roam_duration_02', 'mon_use_days',
                'is_p_app_wx_times', 'zhujiao_time', 'zhujiao_times',
                'mb5', 'mb10', 'mb30', 'mb60', 'ma60', 'total_count',
                'beijiao_times', 'use_days', 'zhujiao', 'beijiao',
                'zhujiao_jt', 'open', 'close', 'open_day', 'cell_num']


def get_all_data(features_file='./data/3月用户相关数据.csv', label_file='./data/3月被投诉用户.csv'):
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


def main():
    get_all_data()


if __name__ == '__main__':
    main()