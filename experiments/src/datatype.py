"""
对features按数据类型分类
"""
from data_utils import get_clean_raw_data


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


if __name__ == '__main__':
    bool_num()
