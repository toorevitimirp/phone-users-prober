from pandas import DataFrame


bool_feature = ['users_3w', 'twolow_users', 'roam_users02', 'roam_users01',
                'vv_type', 'in16_roam_tag']
num_feature = ['roam_call_duration', 'roam_duration_02', 'mon_use_days',
               'is_p_app_wx_times', 'zhujiao_time', 'zhujiao_times',
               'mb5', 'mb10', 'mb30', 'mb60', 'ma60', 'total_count',
               'beijiao_times', 'use_days', 'zhujiao', 'beijiao',
               'zhujiao_jt', 'open', 'close', 'open_day', 'cell_num']


def process_num_feature(raw):
    num = []
    maps_num = {
        'feature': '特征',
        'min': '最小值',
        'max': '最大值',
        'max-min': '最小值和最大值的差',
        'var': '方差',
        'std': '标准差',
        'mean': '平均值',
        'quant_25': '25%',
        'quant_75': '75%',
        'median': '中位数'
    }
    for col in num_feature:
        one = {'feature': col}
        one['min'] = float(raw[col].min())
        one['max'] = float(raw[col].max())
        one['max-min'] = float(one['max'] - one['min'])
        one['var'] = float(raw[col].var())
        one['std'] = float(raw[col].std())
        one['mean'] = float(raw[col].mean())
        one['median'] = float(raw[col].median())
        one['quant_25'] = float(raw[col].quantile(.25))
        one['quant_75'] = float(raw[col].quantile(.75))
        # for k in maps_num.keys():
        #     print(k)
        #     if k != 'feature' or k != 'max-min':
        #         func = getattr(raw[col], k, None)
        #         print(k)
        #         one[k] = func()
        num.append(one)
    return num


def process_bool_feature(raw):
    maps_bool = {
        'zero': '0',
        'one': '1',
        'all': 'all',
        'zero_all': '0/all',
        'one_all': '1/all'
    }

    zero_one = []
    for col in bool_feature:
        grouped = raw.groupby([col])
        count_0 = 0
        count_1 = 0

        unique = raw[col].unique()
        for k0 in [0, '0']:
            if k0 in unique:
                count_0 += grouped.size()[k0]
        for k1 in [1, '1']:
            if k1 in unique:
                count_1 += grouped.size()[k1]

        count_all = raw[col].count()
        one_data = {'feature': col, 'all': int(count_all),
                    'one': int(count_1), 'zero': int(count_0),
                    'zero_all': float(count_0 / count_all),
                    'one_all': float(count_1 / count_all)}
        zero_one.append(one_data)

    return zero_one
