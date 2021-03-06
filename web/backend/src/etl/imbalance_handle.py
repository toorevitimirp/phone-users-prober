import numpy as np
import pandas as pd

from collections import Counter
from etl.dimension_reduction import features_extraction_3d


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
    # 时间很长
    from imblearn.over_sampling import ADASYN
    print(Counter(y))
    X_sampled, y_sampled = ADASYN().fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _random_under_sample(X, y):
    from imblearn.under_sampling import RandomUnderSampler
    rus = RandomUnderSampler(random_state=0, replacement=True)
    print(Counter(y))
    X_sampled, y_sampled = rus.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _near_miss(X, y):
    from imblearn.under_sampling import NearMiss
    versions = [1, 2, 3]
    print(Counter(y))
    nm = NearMiss(version=versions[2])
    X_sampled, y_sampled = nm.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _tomek_links(X, y):
    from imblearn.under_sampling import TomekLinks
    print(Counter(y))
    tl = TomekLinks()
    X_sampled, y_sampled = tl.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _enn(X, y):
    from imblearn.under_sampling import EditedNearestNeighbours
    print(Counter(y))
    enn = EditedNearestNeighbours(random_state=0)
    X_sampled, y_sampled = enn.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _renn(X, y):
    from imblearn.under_sampling import RepeatedEditedNearestNeighbours
    print(Counter(y))
    renn = RepeatedEditedNearestNeighbours(random_state=0)
    X_sampled, y_sampled = renn.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _allnn(X, y):
    from imblearn.under_sampling import AllKNN
    print(Counter(y))
    allknn = AllKNN(random_state=0)
    X_sampled, y_sampled = allknn.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _cnn(X, y):
    from imblearn.under_sampling import CondensedNearestNeighbour
    print(Counter(y))
    cnn = CondensedNearestNeighbour(random_state=0)
    X_sampled, y_sampled = cnn.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _oss(X, y):
    from imblearn.under_sampling import OneSidedSelection
    print(Counter(y))
    oss = OneSidedSelection(random_state=0)
    X_sampled, y_sampled = oss.fit_sample(X, y)

    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _ncr(X, y):
    from imblearn.under_sampling import NeighbourhoodCleaningRule
    print(Counter(y))
    ncr = NeighbourhoodCleaningRule(random_state=0)
    X_sampled, y_sampled = ncr.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _iht(X, y):
    from sklearn.linear_model import LogisticRegression
    from imblearn.under_sampling import InstanceHardnessThreshold
    print(Counter(y))
    iht = InstanceHardnessThreshold(random_state=0,
                                    estimator=LogisticRegression())
    X_sampled, y_sampled = iht.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _smoteenn(X, y):
    from imblearn.combine import SMOTEENN
    print(Counter(y))
    smote_enn = SMOTEENN(random_state=0)
    X_sampled, y_sampled = smote_enn.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def _smotetomek(X, y):
    from imblearn.combine import SMOTETomek
    print(Counter(y))
    smote_tomek = SMOTETomek(random_state=0)
    X_sampled, y_sampled = smote_tomek.fit_sample(X, y)
    print(Counter(y_sampled))
    return X_sampled, y_sampled


def imbalanced_handle(X, y):
    """
    处理数据极度不平衡的情况
    :param X: m×n的np.ndarray,特征集
    :param y: m×1的np.ndarray, 标签
    :return: X:r×n的np.ndarray y:r×1的np.ndarray
    """
    # X_sampled, y_sampled = _smoteenn(X, y)
    # X_sampled, y_sampled = _iht(X, y)
    # X_sampled, y_sampled = _tomek_links(X, y)
    # X_sampled, y_sampled = _near_miss(X, y)
    # X_sampled, y_sampled = _random_under_sample(X, y)
    # X_sampled, y_sampled = _smote(X, y)
    # X_sampled, y_sampled = _adasyn(X, y)
    X_sampled, y_sampled = _random_over_sample(X, y)
    # X_sampled, y_sampled = X, y
    return X_sampled, y_sampled

