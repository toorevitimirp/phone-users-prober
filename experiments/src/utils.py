"""
normalization and wash data
"""
import re
from pandas import DataFrame

bool_features = ['users_3w', 'twolow_users', 'roam_users02', 'roam_users01',
                 'vv_type', 'in16_roam_tag']
num_features = ['roam_call_duration', 'roam_duration_02', 'mon_use_days',
                'is_p_app_wx_times', 'zhujiao_time', 'zhujiao_times',
                'mb5', 'mb10', 'mb30', 'mb60', 'ma60', 'total_count',
                'beijiao_times', 'use_days', 'zhujiao', 'beijiao',
                'zhujiao_jt', 'open', 'close', 'open_day', 'cell_num']


def z_score(data):
    # z-score规范化
    data = (data - data.mean()) / data.std()
    return data


def max_min(clean_data):
    # max-min规范化
    pass


def _is_number(num):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(str(num))
    if result:
        return True
    else:
        return False


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
