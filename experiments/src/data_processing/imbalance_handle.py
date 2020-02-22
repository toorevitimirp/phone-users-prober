import common
import numpy as np
import pandas as pd
from visualization.d3 import draw_3d
from collections import Counter
from data_processing.dimension_reduction import features_extraction_3d
from other.other_utils import beep


def _visualization_sampled_data(X_sampled, y_sampled):
    X_3d = features_extraction_3d(X_sampled)

    df = pd.DataFrame(X_3d)
    df['label'] = pd.Series(y_sampled)
    grouped = df.groupby('label')

    data_1 = grouped.get_group(1)
    data_0 = grouped.get_group(0)

    pos1 = data_1.drop(labels='label', axis=1)
    pos0 = data_0.drop(labels='label', axis=1)

    pos0 = np.array(pos0)
    pos1 = np.array(pos1)

    draw_3d(pos0, pos1)


def _random_over_sample(X, y):
    from imblearn.over_sampling import RandomOverSampler
    print(Counter(y))
    ros = RandomOverSampler(random_state=0)
    X_sampled, y_sampled = ros.fit_sample(X, y)

    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _smote(X, y):
    from imblearn.over_sampling import SMOTE
    kinds = ['borderline1', 'borderline2', 'svm', 'regular']
    print(Counter(y))
    X_sampled, y_sampled = SMOTE().fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _adasyn(X, y):
    beep() # 时间很长
    from imblearn.over_sampling import ADASYN
    print(Counter(y))
    X_sampled, y_sampled = ADASYN().fit_sample(X, y)
    print(Counter(y_sampled))
    beep()
    return X_sampled, y_sampled


def imbalanced_handle(X, y):
    X_sampled, y_sampled = _smote(X, y)
    # X_sampled, y_sampled = _adasyn(X, y)
    # X_sampled, y_sampled = _random_over_sample(X, y)
    # X_sampled, y_sampled = X, y
    return X_sampled, y_sampled


def main():
    from data_processing.data_utils import get_clean_raw_data, num_features
    raw_data = get_clean_raw_data(features_file='../../data/3月用户相关数据.csv',
                                  label_file='../../data/3月被投诉用户.csv')
    X = np.array(raw_data[num_features])
    y = np.array(raw_data['label'])
    X_sampled, y_sampled = imbalanced_handle(X, y)
    _visualization_sampled_data(X_sampled, y_sampled)


if __name__ == '__main__':
    main()
