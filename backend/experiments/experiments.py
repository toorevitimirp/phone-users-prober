# import pandas as pd
from database import get_all_data


def bool_num():
    # 测试feature的数据类型，(bool or numerical)
    bool_feature = []
    num_feature = []
    data = get_all_data('3月')
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
            bool_feature.append(col)
        else:
            num_feature.append(col)
    print(bool_feature, num_feature)


if __name__ == '__main__':
    bool_num()
