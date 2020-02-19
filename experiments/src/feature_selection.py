"""
特征选择
"""
from sklearn.feature_selection import VarianceThreshold

from data_utils import get_clean_raw_data, bool_features, num_features


def variance_threshold():
    raw_data = get_clean_raw_data(features_file='../data/3月用户相关数据.csv',
                                  label_file='../data/3月被投诉用户.csv')

    all_features = bool_features+num_features
    X = raw_data[all_features]
    print('未进行特征选择的数据形状：{}'.format(X.shape))
    sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
    X_select = sel.fit_transform(X)

    print('特征选择后的数据形状：{}'.format(X_select.shape))


def main():
    variance_threshold()


if __name__ == '__main__':
    main()